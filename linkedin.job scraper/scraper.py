from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import matplotlib.pyplot as plt

# ============================
#  ENTER YOUR DETAILS HERE
# ============================
LINKEDIN_EMAIL = "your_email@example.com"      # <-- Replace with your LinkedIn email
LINKEDIN_PASSWORD = "your_password"            # <-- Replace with your LinkedIn password
JOB_KEYWORD = "Python Developer"
JOB_LOCATION = "Chennai"

# ============================
#  Setup Chrome in Incognito
# ============================
options = Options()
options.add_argument("--incognito")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# ============================
#  Login to LinkedIn
# ============================
driver.get("https://www.linkedin.com/login")
time.sleep(2)

# Clear any autofill and type your email/password only
email_box = driver.find_element(By.ID, "username")
email_box.clear()
email_box.send_keys(LINKEDIN_EMAIL)

pass_box = driver.find_element(By.ID, "password")
pass_box.clear()
pass_box.send_keys(LINKEDIN_PASSWORD)

# Click Login
driver.find_element(By.XPATH, "//button[@type='submit']").click()
time.sleep(5)

# ============================
#  Job Search
# ============================
search_url = f"https://www.linkedin.com/jobs/search/?keywords={JOB_KEYWORD}&location={JOB_LOCATION}"
driver.get(search_url)
time.sleep(5)

# Scroll to load more jobs
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# ============================
#  Scrape Jobs
# ============================
soup = BeautifulSoup(driver.page_source, "html.parser")
jobs = soup.find_all("div", class_="base-card")

job_list = []
for job in jobs:
    title = job.find("h3", class_="base-search-card__title")
    company = job.find("h4", class_="base-search-card__subtitle")
    posted = job.find("time")

    job_list.append({
        "Job Title": title.text.strip() if title else "N/A",
        "Company Name": company.text.strip() if company else "N/A",
        "Posted": posted.text.strip() if posted else "N/A"
    })

# ============================
#  Save to CSV
# ============================
df = pd.DataFrame(job_list)
df.drop_duplicates(inplace=True)
df.to_csv("job_data.csv", index=False)
print(" Job data saved to job_data.csv")

# ============================
#  Create Graph
# ============================
job_counts = df["Company Name"].value_counts()

plt.figure(figsize=(10, 6))
job_counts.plot(kind="bar", color="mediumslateblue")
plt.title("Jobs by Company")
plt.xlabel("Company")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.savefig("job_graph.png")
plt.show()

print(" Job graph saved as job_graph.png")

# ============================
#  Close the browser
# ============================
driver.quit()