# Inflation Data Analysis Project

## Introduction

    This project involves analyzing U.S. inflation data, focusing on the Consumer Price Index (CPI) for All Items and Gasoline prices. The goal is to understand how changes in Gasoline prices affect overall price levels. The project consists of several tasks, each addressing specific questions and objectives.

## Folder Structure

    - **Outputs & Tests:** Contains all the outputs of the scripts and testing scripts. Each file is prefixed with the corresponding question number.

    - **Codes:** Contains the answers in .py file (not included PDFs answers and tests).  Each file is name after the question and its number.

    - **Answer_Case_JGP:** Contains the answers to Questions 3 and 4, along with detailed analysis.


## Project Structure

    ### Question 1: Data Extraction

        - **Objective:** Obtain U.S. inflation series (CPI) from the Bureau of Labor Statistics (BLS) via API.
        - **Data Sources:**
        - CPI All items, seasonally adjusted (CUSR0000SA0)
        - CPI All items, less food and energy, seasonally adjusted (CUSR0000SA0L1E)
        - CPI Gasoline (all types), seasonally adjusted (CUSR0000SEGA)
        - **Output:** Save the processed data in a CSV file (cpi_data.csv) with columns corresponding to the series and rows representing observations over time. 




    ### Question 2: Data Visualization

        - **Objective:** Using Plotly in Python, develop a chart displaying the All items, less food and energy, seasonally adjusted price series with year-over-year percentage variation using the monthly data from 2019 to the present.
        - **Data Sources:**
            - cpi_data.csv file
        - **Output:** A Plotly chart that keeps the frequency monthly.


    ### Question 3: Automation Description

        - **Objective:** Describe how to automate the process of extracting the data.


    ### Question 4: Relationship Analysis

        - **Objective:** Explain how to relate the price series (All items) with the Gasoline (Gasoline) price series.
        - **Data Sources:**
            - cpi_data.csv file


    ### Bonus Question: FastAPI Implementation

        - **Objective:** Implement an application using FastAPI to allow requests to the data stored in the CSV file.
        - **Output:** FastAPI application with endpoints to retrieve the data.





## How to Run

    ### Install Dependencies
        pip install -r requirements.txt

    ## Run code
        python Codes/Question_1.py
        python Codes/Question_2.py
        python Codes/Question_4.py
        python Codes/Question_bonus

    ## To test the FastAPI
        *To run the test it is necessary to install the package uvicorn and add the .exe to the PATH*
        python Codes/Question_bonus
        uvicorn Codes/Question_bonus:app
        python Outputs_&_Tests/question_bonus_testing



## Dependencies
    -   pandas
    -   statsmodels
    -   matplotlib
    -   fastapi
    -   uvicorn
    -   plotly
    -   scipy
    -   numpy
