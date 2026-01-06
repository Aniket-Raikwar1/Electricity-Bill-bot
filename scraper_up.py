import time
import os
import glob
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class BillScraper:
    def __init__(self):
        # Configuration
        self.download_dir = os.path.join(os.getcwd(), "My_Electricity_Bills")
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        # --- CHROME OPTIONS FOR AWS T3.MICRO ---
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless=new") # <--- UPDATED: Modern headless mode
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu") # <--- ADDED: Safer for servers without graphics cards
        self.chrome_options.add_argument("--window-size=1920,1080")
        
        # Preferences to auto-download PDFs
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
            "profile.default_content_settings.popups": 0
        }
        self.chrome_options.add_experimental_option("prefs", prefs)

    def get_latest_file(self):
        """Helper to find the most recently downloaded file"""
        # We filter out .crdownload files to ensure we only get finished files
        files = [f for f in glob.glob(os.path.join(self.download_dir, "*")) if not f.endswith('.crdownload')]
        if not files: return None
        return max(files, key=os.path.getctime)

    def fetch_bill(self, ivrs_number):
        """
        Main logic to fetch the bill. 
        """
        # 1. CACHE CHECK
        current_month_str = datetime.now().strftime('%b_%Y')
        expected_filename = os.path.join(self.download_dir, f"Bill_{ivrs_number}_{current_month_str}.pdf")

        if os.path.exists(expected_filename):
            print(f"✅ Cache Hit: Bill for {ivrs_number} already exists.")
            return expected_filename

        # 2. START BROWSER
        driver = webdriver.Chrome(options=self.chrome_options)
        
        try:
            print(f"🚀 Opening Website for IVRS: {ivrs_number}")
            driver.get("https://mpwzservices.mpwin.co.in/westdiscom/home")
            
            # --- STEP 1: ENTER IVRS ---
            wait = WebDriverWait(driver, 20)
            ivrs_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='ivrs']")))
            ivrs_box.clear()
            ivrs_box.send_keys(ivrs_number)

            # --- STEP 2: CLICK SUBMIT ---
            print("🖱️ Clicking Submit...")
            submit_btn = driver.find_element(By.XPATH, "//input[@type='submit' and contains(@value, 'View & Pay')]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(1)
            
            try:
                submit_btn.click()
            except:
                driver.execute_script("arguments[0].click();", submit_btn)

            time.sleep(2)
            new_windows = driver.window_handles
            if len(new_windows) > 1:
                driver.switch_to.window(new_windows[-1])

            # --- STEP 3: FIND DOWNLOAD BUTTON ---
            print("⏳ Looking for download button...")
            final_download_btn = wait.until(EC.any_of(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'View Latest Month Bill')]")),
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@value, 'View Latest Month Bill')]")),
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'View Latest Month Bill')]"))
            ))

            # Trigger Download
            # Note: We take a snapshot of files BEFORE clicking
            initial_files = set(os.listdir(self.download_dir))
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", final_download_btn)
            final_download_btn.click()

            # --- STEP 4: SAFER WAIT LOOP ---
            print("⬇️ Downloading...")
            seconds_waited = 0
            download_complete = False
            
            while seconds_waited < 40: # Increased timeout slightly
                time.sleep(1)
                current_files = set(os.listdir(self.download_dir))
                new_files = current_files - initial_files
                
                # Check if we have a new file AND it is not a temporary .crdownload file
                if new_files:
                    latest = max([os.path.join(self.download_dir, f) for f in new_files], key=os.path.getctime)
                    if not latest.endswith(".crdownload") and not latest.endswith(".tmp"):
                        download_complete = True
                        break
                
                seconds_waited += 1

            if download_complete:
                latest_file = self.get_latest_file()
                if latest_file:
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
    # Replace with a real number for testing
    scraper.fetch_bill("N3355009057")