# Website Data Scraper

## Overview
Website Data Scraper is a Python-based tool that scrapes a specified website URL and extracts data into CSV format. The extracted data includes image URLs and information stored within specific HTML tags (e.g., `<h1>`, `<p>`, etc.). This project is ideal for those looking to collect structured data from web pages for analysis or storage.

## Features
- Extracts text data from HTML tags such as `<h1>`, `<p>`, and more.
- Extracts image URLs.
- Stores extracted data in CSV format.
- Easy configuration for different websites and HTML structures.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation
### Prerequisites/dependencies
-pip >24.1 version
- Python 3.x
- playwright==1.41.1
-requests==2.31.0
-beautifulsoup4==4.12.2
- `pip` package manager

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/website-data-scraper.git
   cd website-data-scraper
