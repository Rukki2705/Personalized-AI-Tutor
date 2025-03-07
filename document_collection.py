import os
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

# Download NLTK data (first-time run)
nltk.download('punkt_tab')
nltk.download('stopwords')

# Define the target URLs for scraping
URLS = [
    # Mathematics
    "https://www.khanacademy.org/math",
    "https://en.wikipedia.org/wiki/Mathematics",
    "https://mathworld.wolfram.com/",
    
    # Physics
    "https://www.khanacademy.org/science/physics",
    "https://en.wikipedia.org/wiki/Physics",
    "http://hyperphysics.phy-astr.gsu.edu/hbase/hframe.html",
    
    # Computer Science
    "https://www.khanacademy.org/computing/computer-science",
    "https://en.wikipedia.org/wiki/Computer_science",
    "https://www.geeksforgeeks.org/computer-science/",
    
    # Biology
    "https://www.khanacademy.org/science/biology",
    "https://en.wikipedia.org/wiki/Biology",
    "https://www.ncbi.nlm.nih.gov/",
    
    # Chemistry
    "https://www.khanacademy.org/science/chemistry",
    "https://en.wikipedia.org/wiki/Chemistry",
    "https://www.chemguide.co.uk/",
    
    # Electrical Engineering
    "https://www.khanacademy.org/science/electrical-engineering",
    "https://en.wikipedia.org/wiki/Electrical_engineering",
    
    # Mechanical Engineering
    "https://www.khanacademy.org/science/mechanical-engineering",
    "https://en.wikipedia.org/wiki/Mechanical_engineering",
    
    # Economics
    "https://www.khanacademy.org/economics-finance-domain/microeconomics",
    "https://en.wikipedia.org/wiki/Economics",
    
    # Psychology
    "https://www.khanacademy.org/science/health-and-medicine/behavioral-biology",
    "https://en.wikipedia.org/wiki/Psychology"
]

# Directory to save scraped content
DATA_DIR = "scraped_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Function to clean and preprocess text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\[.*?\]', '', text)  # Remove references [1], [2], etc.
    text = text.strip()
    sentences = sent_tokenize(text)  # Split into sentences
    filtered_sentences = [s for s in sentences if len(s) > 30]  # Remove very short sentences
    return " ".join(filtered_sentences)

# Function to scrape and extract text content
def scrape_text(url):
    print(f"Scraping: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract text from paragraphs
    paragraphs = soup.find_all('p')
    text = " ".join([p.get_text() for p in paragraphs])
    
    # Clean the extracted text
    return clean_text(text)

# Store all scraped data
scraped_data = {}

for url in URLS:
    text_content = scrape_text(url)
    if text_content:
        scraped_data[url] = text_content

# Save the scraped data in JSON format
output_file = os.path.join(DATA_DIR, "scraped_content.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=4)

# Convert to CSV format for easier indexing
df = pd.DataFrame(scraped_data.items(), columns=["URL", "Content"])
df.to_csv(os.path.join(DATA_DIR, "scraped_content.csv"), index=False)

print(f"Scraping complete! Data saved in {DATA_DIR}")
