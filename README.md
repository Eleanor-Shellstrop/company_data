# Company Spreadsheets

by Anne Ensign

## About

This is a project for Code Louisville's Data Analysis Course 2.  

### Scenario

You are recently hired to a company that hasn't been keeping all their records updated. You notice a CSV with all orders for the last 2 years, which is up to date. You also notice a CSV with contact people for the companies, but there are many more companies with orders than contacts on this file. Also, a database would be a better way to store these records.

1. Create a program to scan all the CSVs in one folder.
2. Update the tables to be clean and consistant.
3. Extract the data to evaluate.
4. Create visuals for the other departments.
5. Make sure the program can update the data every time it's run when new info is added to the CSVs.

**Spreadsheets**

Data was generated through [Mockaroo](https://www.mockaroo.com).

`original_csvs` folder contains the CSVs as originally uploaded. Any transformation will occur to the CSVs in the `csv` folder.

## Running the Program

Python 3 is required to run this program. I wrote these scripts with version 3.9.6 installed, and at the time I'm writing this, any version 3.6 or below is EOL.

If you need to download or update Python, [click here](https://www.python.org).

### Main Program

The files to try the program are in the zip file `TRY_IT`.

1. Download the repo or only the `TRY_IT` file, or clone.
2. Save to location of your choice.
3. Extract all files from the zip folder `TRY_IT`.
4. In your command line, navigate to the root folder in the repo.
5. Recommended: Create a virtual environment to run the program.
6. Run the requirements:

     **CONDA:** 

     `pip install -r requirements.txt`

     **Windows:**

     `py -m pip install -r requirements.txt`

     **Unix/macOS:**

     `python -m pip install -r requirements.txt`

     If you do not have Anaconda installed, make sure to enter the following commands in your command line once you've navigated to the repo folder:
       
     	pip install notebook

     	pip install pandas
	
7. From the root folder `TRY_IT`, navigate to the `python` folder.
8. Run the `db_auto.py` file first with command:

		python db_auto.py

9. Once that file is complete, remaining in the `python` folder, run the next file:

		python sql_pandas.py

You should see other folders appear: `database`, `datasets`, and `tableau`. Your CSVs are now cleaned up tables in a database!

### Running Tests

You can also run unit tests to make sure your pandas methods and python function are working correctly.

1. From your saved repo, navigate to `TRY_IT/test/python`.
2. Run files one at a time:

	`python test_pandas.py`

	`python test_python.py`

     `python test_sql.py`

The `test_pandas.py` will log your unit test results with a timestamp in the `text/log.txt` file.

## Tableau

My Tableau profile has visuals for these databases. [CLICK HERE](https://public.tableau.com/app/profile/anne.ensign/viz/Company_16474575907250/Dashboard-2YearReview_1) to visit my page.

## Acknowledgements

While this code and project is my own, I found a lot of helpful information about structuring the process from [Nate from StrataScratch](https://github.com/Strata-Scratch/csv_to_db_automation).