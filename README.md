# Election Data Analysis Repository

## Overview
This repository contains scripts and data files used for scraping and analyzing election results from various websites. The data scraping is performed using Selenium, and the analysis is carried out using Python.

## Repository Structure

  - `election_resultsBJP.xlsx` - Election results for the BJP party.
  - `election_resultsINC.xlsx` - Election results for the INC party.
  - `election_resultsIND.xlsx` - Election results for independent candidates.
  - `election_resultsNCP.xlsx` - Election results for the NCP party.
  - `election_resultsNPEP.xlsx` - Election results for the NPEP party.
  - `election_resultsPPA.xlsx` - Election results for the PPA party.
  - `election_results_arunachalam.xlsx` - Election results for Arunachalam.
  - `election_results_sikkim.xlsx` - Election results for Sikkim.
  - `excel_final.py` - Script for scraping the constituencies data.
  - `kalvium_2.py` - Script for scraping the first page.
- `README.md` - This file.

## Prerequisites

- Python 3.x
- Selenium
- Pandas
- xlsxwriter

## Setup

1. **Clone the repository:**

2. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Download the necessary web drivers for Selenium and ensure they are available in your PATH.**

## Data Scraping

The data scraping is done using Selenium. Ensure you have the appropriate web drivers installed and available in your PATH. The scraping scripts are not included here but can be adapted based on the Selenium setup provided.

## Data Analysis

### `excel_final.py`
This script performs the final analysis and aggregation of the election results data.

**Usage:**

```bash
python scripts/excel_final.py
```

### `kalvium_2.py`
This script handles the initial data cleaning and preparation.

**Usage:**

```bash
python scripts/kalvium_2.py
```


## Results

The analysis results will be saved in the output directory, which will be created by the scripts if it does not already exist. The results will include various insights and visualizations derived from the election data.
