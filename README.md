# QS World University Rankings 2025 - Web Scraping, Data Cleaning, and Visualization

## Project Overview
This project involves web scraping the **QS World University Rankings 2025** from [TopUniversities](https://www.topuniversities.com/world-university-rankings), cleaning the extracted data, and visualizing insights using **Tableau**. The ranking is based on multiple parameters, such as faculty citations, academic reputation, employer reputation, and international research collaborations.

## Workflow
1. **Web Scraping:** Scraped QS World University Rankings 2025 from **20 pages**.
2. **Data Cleaning:** Removed duplicates, handled missing values, and structured the dataset properly.
3. **Visualization:** Created interactive Tableau visualizations to analyze ranking factors and provide insights.

## How to Run the Scraper
### Prerequisites
Ensure you have Python installed along with required dependencies.

### Installation
Clone the repository and install dependencies:
```bash
git clone <repository_url>
cd <repository_folder>
pip install -r requirements.txt
```

### Running the Scraper
Execute the Python script to start scraping:
```bash
python university_scraper.py
```
- The script will take approximately **2 hours** to scrape all the data.
- The data will be saved as a **CSV file**.
- The same script can be used for the **2024 QS Ranking** with minor modifications.

## Data Cleaning
Once data is collected, clean it using the **data_cleaning notebook**:
- Removed **duplicates**
- Handled **null values**
- Standardized **data formats**

## Visualization
After cleaning, the dataset was used for Tableau visualizations. Key insights include:
- **MIT ranks first** due to high scores across all ranking parameters.
- **Highest faculty citations** did not correlate with the **top rank**.
- **Bangladeshi universities** should focus on increasing **research output** and **international collaborations** to improve ranking.

### Tableau Dashboard
You can explore the interactive Tableau visualization here:
[QS Ranking 2025 Insights](https://public.tableau.com/views/QSRanking2025Insights/Dashboard1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## Future Improvements
- Automate data updates for **yearly rankings**.
- Expand visualizations with **comparative analysis over multiple years**.


