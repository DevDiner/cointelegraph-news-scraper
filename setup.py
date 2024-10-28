from setuptools import setup, find_packages

setup(
    name='cointelegraph_news_scraper',
    version='1.0.0',
    description='Cointelegraph_news_scraper',
    author='DevDiner',
    author_email='demosampleacc@gmail.com',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'fastapi',
        'uvicorn',
        'motor',
        'beautifulsoup4',
        'python-dotenv',
        'playwright'
    ],
)
