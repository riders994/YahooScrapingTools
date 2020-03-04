from setuptools import setup, find_packages

setup(
    name="YahooScrapingTools",
    version='1.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'objectpath', 'pytz', 'yahoo_oauth', 'docopt', 'yahoo_fantasy_api'
    ],
    python_requires='>=3',
)
