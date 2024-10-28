#services/scraper_service.py
#to esure system file path direct to this current path for the code to be run   
import sys
import json
sys.path.append('/root/folder/cointelegraph_news_scraper')

import asyncio
from datetime import datetime, timedelta
import pytz  # For timezone handling
import re  # For extracting numbers from relative time strings
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from services.mongodb_service import db
from utils.log_utils import setup_logging
from config import config  # Importing configuration settings

logger = setup_logging()

# Function to get the system's local time zone (Kuala Lumpur)
def get_system_timezone():
    return pytz.timezone('Asia/Kuala_Lumpur')  # Kuala Lumpur time zone

# Function to convert relative time (e.g., '1 hour ago') to local time (Kuala Lumpur)
def convert_relative_time_to_utc(relative_time_str):
    try:
        system_tz = get_system_timezone()  # Get Kuala Lumpur timezone
        current_time = datetime.now(system_tz)  # Use local time as the reference time

        if "hour" in relative_time_str:
            hours_ago = int(re.findall(r'\d+', relative_time_str)[0])
            return current_time - timedelta(hours=hours_ago)
        elif "minute" in relative_time_str:
            minutes_ago = int(re.findall(r'\d+', relative_time_str)[0])
            return current_time - timedelta(minutes=minutes_ago)
        elif "day" in relative_time_str:
            days_ago = int(re.findall(r'\d+', relative_time_str)[0])
            return current_time - timedelta(days=days_ago)
        elif "week" in relative_time_str:
            weeks_ago = int(re.findall(r'\d+', relative_time_str)[0])
            return current_time - timedelta(weeks=weeks_ago)
        else:
            logger.error(f"Unable to parse relative time string: {relative_time_str}")
            return None
    except Exception as e:
        logger.error(f"Error converting relative time to local time: {e}")
        return None

# Function to handle different date formats and ensure time is in Kuala Lumpur
def parse_date_string(date_str):
    try:
        system_tz = get_system_timezone()  # Get Kuala Lumpur timezone
        if 'T' in date_str:
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC).astimezone(system_tz)
        else:
            return datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=pytz.UTC).astimezone(system_tz)
    except ValueError as e:
        logger.error(f"Error parsing date string: {e}")
        return None

# Function to return the original datetime object (in Kuala Lumpur time zone)
def format_timestamp_to_string(timestamp):
    return timestamp  # Return the original datetime object

async def fetch_page(page, url):
    logger.info(f"Fetching URL: {url}")
    try:
        await page.goto(url, timeout=config.PAGE_LOAD_TIMEOUT)  # Use config for timeout
        return await page.content()
    except Exception as e:
        logger.error(f"Error fetching the page {url}: {e}")
        return None

async def extract_article_links(page, home_url):
    html = await fetch_page(page, home_url)
    if html is None:
        logger.warning("Failed to fetch article links.")
        return []
    soup = BeautifulSoup(html, 'html.parser')
    article_links = [home_url.rstrip('/') + link.get('href') for link in soup.select('a.block.hover\\:underline[target="_self"]') if link.get('href')]
    logger.info(f"Found {len(article_links)} article links.")
    return article_links

async def scrape_article(page, url):
    html = await fetch_page(page, url)
    if not html:
        logger.warning(f"No HTML content fetched for {url}")
        return None

    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.select_one('h1')
    content_tags = soup.select('p, blockquote')
    timestamp_tag = soup.select_one('time')

    title = title_tag.get_text(strip=True) if title_tag else "No title found"

     # Exclude content with specific classes, <em><strong> elements, and identified components
    content = "\n".join(
        [p.get_text(strip=True) for p in content_tags
        if ('privacy-policy__text' not in p.get('class', []) and
            'post-content__disclaimer' not in p.get('class', []) and
            'promo-button-disclaimer__text_oYzpz' not in p.get('class', []) and
            'mint-in-article-widget-collect-title' not in p.get('data-testid', '') and
            '!mt-0 text-xs font-semibold leading-4 text-fg-primaryDefault' not in p.get('class', []) and
            '!mt-0 text-base font-semibold leading-5 text-fg-inverted' not in p.get('class', []) and
            '!mt-0 text-xs leading-4 text-[#98A4AA]' not in p.get('class', []) and
            'newsletter-subscription-form-enjoy_uvMCq' not in p.get('class', []) and
            'newsletter-subscription-form-title_7jvjJ' not in p.get('class', []) and
            'newsletter-subscription-form-description_wtZv+' not in p.get('class', []) and
            'newsletter-subscription-form-tos_lBW2V' not in p.get('class', []) and
            'text-[#98A4AA]' not in p.get('class', []) and
            'Terms of Services and Privacy Policy' not in p.get_text(strip=True) and  # Filter out links to terms
            p.name != 'span' and
            not p.find('em', recursive=False) and not p.find('strong', recursive=False))]
    ) if content_tags else "No content found"

    date = timestamp_tag.get('datetime') if timestamp_tag else None
    timestamp_text = timestamp_tag.get_text(strip=True) if timestamp_tag else None

    # Convert relative timestamp (e.g., '1 hour ago') to actual UTC datetime
    formatted_timestamp = convert_relative_time_to_utc(timestamp_text) if timestamp_text else None

    # If no relative timestamp, fall back to the datetime provided in the `date` field
    if not formatted_timestamp and date:
        formatted_timestamp = parse_date_string(date)
    elif not formatted_timestamp:
        formatted_timestamp = datetime.now(pytz.UTC)  # Fallback to current time
	


    return {
        'title': title,
        'content': content,
        'link': url,
        'date': date,
        'timestamp': format_timestamp_to_string(formatted_timestamp),  # Ensure it's a datetime object
    }

async def scrape_all_articles(home_url, max_articles=19):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=2000)
        context = await browser.new_context(viewport={"width": 1280, "height": 900})
        page = await context.new_page()

        article_links = await extract_article_links(page, home_url)
        articles = []

        for link in article_links:
            article_data = await scrape_article(page, link)
            if article_data:
                articles.append(article_data)

        latest_articles = articles[:max_articles]

        await page.close()
        await browser.close()

    return latest_articles

async def collect_articles():
    articles = await scrape_all_articles(config.SCRAPER_URL)
    articles = [article for article in articles if article['title'] and article['content']]

    # Sort articles by timestamp (latest first) before inserting into MongoDB
    sorted_articles = sorted(articles, key=lambda x: x['timestamp'], reverse=True)

    inserted_articles = []

    for article in sorted_articles:
        try:
            logger.info(f"Checking for duplicates in MongoDB with link: {article['link']}")
            existing_article = await db.find_one({"link": article['link']})

            if existing_article is None:
                if article['timestamp'] and isinstance(article['timestamp'], datetime):
                    result = await db.insert_one({
                        **article,
                        'timestamp': article['timestamp']  # Insert the datetime object
                    })
                    logger.info(f"Inserted article: {article['title']} into MongoDB")
                    inserted_articles.append(article)
                else:
                    logger.warning(f"Article '{article['title']}' does not have a valid timestamp, skipping insertion.")
            else:
                logger.info(f"Duplicate article found, not inserting: {article['title']}")
        except Exception as e:
            logger.error(f"Error inserting article '{article['title']}' : {e}")

    # Prepare the response for FastAPI, convert `datetime` to string
    response_articles = [
        {**article, 'timestamp': article['timestamp'].isoformat() if article['timestamp'] else None}
        for article in inserted_articles
    ]

    if not inserted_articles:
        logger.info("No new articles were found. The latest news has already been updated.")

    try:
        with open('cointelegraph_articles.json', 'w', encoding='utf-8') as f:
            json.dump(response_articles, f, ensure_ascii=False, indent=4, default=str)
            logger.info(f"Inserted articles saved to cointelegraph_articles.json with {len(response_articles)} articles.")
    except Exception as e:
        logger.error(f"Error saving articles to JSON file: {e}")

    return response_articles

if __name__ == "__main__":
    asyncio.run(collect_articles())
