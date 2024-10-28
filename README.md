# Cointelegraph News Scraper

A web scraper that fetches the latest articles from Cointelegraph, stores them in MongoDB, and serves them via a FastAPI REST API.

## Features
- Scrapes news articles from Cointelegraph.
- Stores the data in a MongoDB collection.
- Provides a FastAPI-based API to fetch the articles.
- Handles time zones (Kuala Lumpur) and converts relative timestamps.
- Logs scraping and API requests.
- Continuous Integration (CI) using GitHub Actions.
- Supports deployment to Google Cloud Run.

## Requirements

- Python 3.10+
- MongoDB
- Playwright
- FastAPI
- Motor (async MongoDB driver)
- Uvicorn

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/DevDiner/cointelegraph-news-scraper.git
    cd cointelegraph-news-scraper
    ```

2. **Install dependencies**:
    Install the required dependencies via pip:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

3. **Configure environment variables**:
    Create a `.env` file by copying `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Update the `.env` file with your MongoDB URI and other configurations:
    ```bash
    MONGO_URI=mongodb://localhost:27017
    DB_NAME=crypto_news
    MONGO_COLLECTION=cointelegraph-news
    LOG_LEVEL=info
    SCRAPER_URL=https://www.cointelegraph.com/
    PAGE_LOAD_TIMEOUT=300000
    PLAYWRIGHT_HEADLESS=true
    PLAYWRIGHT_SLOW_MO=2000
    ```

4. **Install Playwright**:
    Run the following command to install the Playwright browsers:
    ```bash
    python -m playwright install
    ```

5. **Run the FastAPI server**:
    Start the FastAPI server using Uvicorn:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8080
    ```

6. **Access the API**:
    Navigate to `http://localhost:8080/docs` to view the FastAPI auto-generated documentation.

7. **Run the Scraper via the API**:
    Scrape articles using the following endpoint:
    ```
    GET /api/v1/scraper/scrape
    ```
    This will scrape the latest articles and return them in a sorted order (latest first).

---

## API Endpoints

- **GET** `/api/v1/scraper/scrape`: Triggers the scraping of the latest articles from Cointelegraph and returns the latest sorted articles.
  
Example response:
```json
[
  {
    "title": "Latest News Title",
    "content": "Article content here...",
    "date": "2024-10-12",
    "timestamp": "2024-10-12T18:37:34.029447+08:00",
    "link": "https://www.cointelegraph.com/news/some-news-article"
  }
]
```

---

## Deployment to Google Cloud Run

You can deploy the application to Google Cloud Run for scalable, serverless hosting.

### Steps:

1. **Authenticate with Google Cloud**:
    ```bash
    gcloud init
    ```

2. **Enable Cloud Run and Cloud Build APIs**:
    ```bash
    gcloud services enable run.googleapis.com cloudbuild.googleapis.com
    ```

3. **Build and Push Docker Image**:
    ```bash
    docker build -t gcr.io/YOUR_PROJECT_ID/cointelegraph-news-scraper .
    docker push gcr.io/YOUR_PROJECT_ID/cointelegraph-news-scraper
    ```

4. **Deploy to Cloud Run**:
    ```bash
    gcloud run deploy cointelegraph-news-scraper \
    --image gcr.io/YOUR_PROJECT_ID/cointelegraph-news-scraper \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
    ```

5. **Access the Deployed Service**:
    After deployment, you will receive a URL where the service is available.

---

## Continuous Integration/Continuous Deployment (CI/CD)

This project is set up with **GitHub Actions** to automate testing, building, and deploying the scraper to Google Cloud Run.

### Setting up CI/CD

1. **Configure GitHub Secrets**:
   Add your Google Cloud credentials and project details as GitHub Secrets:
   - `GCP_PROJECT_ID`: Your Google Cloud project ID.
   - `GCP_SA_KEY`: Your Google service account JSON key.
   - `GCP_REGION`: The region where you will deploy (e.g., `us-central1`).

2. **Trigger CI/CD Pipeline**:
   Push changes to the `main` branch or create a pull request to trigger the CI/CD pipeline.

---

## Future Improvements

The current project can be further enhanced in several ways:

1. **Unit Testing**: 
   - Implement unit tests for core functionality (e.g., scraping, database insertion) to ensure that future changes don't break the application. Testing libraries such as `pytest` can be integrated for this purpose.

2. **Flexible Scraping Strategy**:
   - Externalize the scraping logic, such as CSS selectors, into configuration files or databases to allow scraping of different websites without changing the core logic.
   - Implement a scraping strategy pattern for handling various website structures.

3. **Error Handling Enhancements**:
   - Introduce more granular error handling for specific cases such as `TimeoutError`, `ConnectionError`, and other scraping-related exceptions. This will make the application more robust and reliable.
   
4. **Caching Layer**:
   - Add a caching layer to avoid redundant scraping of articles that are already in the database. This can be achieved by storing the last-scraped timestamp and skipping articles that were fetched after that timestamp.

5. **Rate Limiting and Retry Mechanism**:
   - Implement rate limiting and automatic retries for failed scraping attempts to prevent bans from target websites and ensure the scraper runs more smoothly in the event of temporary failures.

6. **Dockerization**:
   - Add Docker support to containerize the application for easier deployment. This will allow the application to be deployed consistently across different environments.

7. **Pagination Support for the API**:
   - Implement pagination in the FastAPI endpoints to allow clients to retrieve articles in batches rather than all at once, improving performance for large datasets.

8. **CI/CD Integration**:
   - Set up Continuous Integration and Continuous Deployment (CI/CD) pipelines with tools like GitHub Actions or Jenkins to automate testing, linting, and deployment processes.

9. **Advanced Logging and Monitoring**:
   - Improve logging by integrating with external services like ELK (Elasticsearch, Logstash, Kibana) or cloud logging services to better track application behavior.
   - Add monitoring tools like Prometheus and Grafana for real-time performance insights.

10. **API Security**:
    - Implement authentication and authorization for the FastAPI endpoints to control access to the data. This could be done using JWT (JSON Web Tokens) or OAuth.

11. **Timezone and Locale Configuration**:
    - Provide more flexibility for different time zones and locales by making the time zone conversion dynamic, allowing users to specify their own time zone.

---

## License

MIT License