import time
import os
import glob
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class BillScraper:
    def __init__(self):
        # Configuration
        self.download_dir = os.path.join(os.getcwd(), "My_Electricity_Bills")
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        # Chrome Options
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--headless") # Uncomment to run invisible
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--window-size=1920,1080")
        
        # specific prefs to auto-download PDFs without asking
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
            "profile.default_content_settings.popups": 0
        }
        self.chrome_options.add_experimental_option("prefs", prefs)

    def get_latest_file(self):
        """Helper to find the most recently downloaded file"""
        files = glob.glob(os.path.join(self.download_dir, "*"))
        if not files: return None
        return max(files, key=os.path.getctime)

    def fetch_bill(self, ivrs_number):
        """
        Main logic to fetch the bill. 
        Returns: Path to the downloaded PDF or None.
        """
        
        # 1. CACHE CHECK: Don't download if we already have it for this month
        current_month_str = datetime.now().strftime('%b_%Y')
        expected_filename = os.path.join(self.download_dir, f"Bill_{ivrs_number}_{current_month_str}.pdf")

        if os.path.exists(expected_filename):
            print(f"✅ Cache Hit: Bill for {ivrs_number} already exists.")
            return expected_filename

        # 2. START BROWSER
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        
        try:
            print(f"🚀 Opening Website for IVRS: {ivrs_number}")
            driver.get("https://mpwzservices.mpwin.co.in/westdiscom/home")
            driver.maximize_window()

            # --- STEP 1: ENTER IVRS ---
            wait = WebDriverWait(driver, 20)
            ivrs_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='ivrs']")))
            ivrs_box.clear()
            ivrs_box.send_keys(ivrs_number)

            # --- STEP 2: CLICK SUBMIT ---
            print("🖱️ Clicking Submit...")
            submit_btn = driver.find_element(By.XPATH, "//input[@type='submit' and contains(@value, 'View & Pay')]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1) # Small pause for scroll to finish
            
            # Handle window switching
            old_windows = driver.window_handles
            try:
                submit_btn.click()
            except:
                driver.execute_script("arguments[0].click();", submit_btn)

            time.sleep(2) # Wait for potential new tab
            new_windows = driver.window_handles
            
            if len(new_windows) > len(old_windows):
                print("🔀 Switching to new tab...")
                driver.switch_to.window(new_windows[-1])

            # --- STEP 3: FIND DOWNLOAD BUTTON ---
            print("⏳ Looking for download button...")
            final_download_btn = wait.until(EC.any_of(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'View Latest Month Bill')]")),
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@value, 'View Latest Month Bill')]")),
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'View Latest Month Bill')]"))
            ))

            # Trigger Download
            initial_files_count = len(os.listdir(self.download_dir))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", final_download_btn)
            final_download_btn.click()

            # --- STEP 4: WAIT FOR FILE ---
            print("⬇️ Downloading...")
            seconds_waited = 0
            while len(os.listdir(self.download_dir)) == initial_files_count and seconds_waited < 30:
                time.sleep(1)
                seconds_waited += 1

            if seconds_waited < 30:
                # File downloaded successfully
                latest_file = self.get_latest_file()
                if latest_file:
                    # Rename it to be specific to this user and month
                    os.rename(latest_file, expected_filename)
                    return expected_filename
            else:
                print("❌ Timed out waiting for file download.")
                return None

        except Exception as e:
            print(f"❌ Error: {e}")
            return None
        finally:
            driver.quit()

# Testing block
if __name__ == "__main__":
    scraper = BillScraper()
    # Test with a real number
    scraper.fetch_bill("N3355009057")