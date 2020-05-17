# INST414-Final
Many new graduates who are looking for jobs in the tech industry do not have a clear way of knowing which locations they should be focusing on in their job search or which potential companies have qualities that they are looking for. People generally want to work at companies that are well rated, have good work atmosphere and more. A great number of factors tie into how a well a company’s rating is, such as their location, the difficulty of their interviews, the company’s size, its revenue, and much more. This report aims to analyze these factors and examine how well they predict a company’s rating. A company overall ratings on Glassdoor; the location; the size of the company; its revenue; whether they have Glassdoor awards; whether they have awards outside of Glassdoor; and their interview difficulty are factors that will be analyzed in order to answer the question: Is there a trend in better rated tech companies across the United States, where some regions have better rated companies than others? By knowing which areas in the United States have more better rated companies, new graduates can then look for careers in those locations and secure a good job that they would be happy working at. Results from the report suggests that there is a trend and that the location of a company may be used to determine a company’s ratings. Using the results from the analysis, new graduates can also lookout for companies of a certain size, revenue, etc., to determine or predict a company’s rating. This report will describe the data that was used; explain the methods behind the analysis; explain the analysis; describe the results that were found; and conclude on the findings.
## Data
### Description of Data
The dependent variable for the analysis is company rating. This is the overall rating of each Information Technology (IT) company on Glassdoor, on a scale of 1-5. They are determined by employee feedback or reviews, and an algorithm with an emphasis on recency of reviews is used to calculate the rating. The independent variables are composed of location, company size, revenue, Glassdoor awards, other awards, and interview difficulty. 
#### Location
This variable is the location of a company’s office location. In order to analyze this, the variable was changed into levels, where a value or state would be assigned to either West (WA, OR, CA, MT, ID, WY, NV, UT, CO, NM, AZ, AK, HI), Northeast (PA, NJ, NY, CT, RI, MA, VT, NH, ME), Midwest (ND, SD, NE, KS, MO, IA, MN, IL, WI, IN, OH, MI), South (TX, OK, AR, LA, MS, AL, GA, FL, TN, SC, NC, KY, VA, WV, DC, MD, DE), or other. 
#### Company Size
Company size is the number of employees in a company and is categorized into three categories: Small (<201), Medium (201 - 1001), and Large (>1,000).
#### Revenue
The revenue variable is how much money (USD) a company makes per year.
#### Glassdoor Awards
The Glassdoor Awards variable determines whether or not a company has an award from Glassdoor, such as being apart of the best places to work, having a top CEO, etc. ‘0’ being that the company does not have a Glassdoor Award and ‘1’ being that a company does. 
#### Other Awards
The Other Awards variable determines whether or not a company has an award outside from Glassdoor, such being among Fortune’s best places to work. ‘0’ being that the company does not have other awards and ‘1’ being that a company does.
#### Interview Difficulty
The interview difficulty variable is how difficult a company’s job interviews are on a point scale of 1 to 5. The rating is calculated from interview reviews of a company on Glassdoor from employees or potential employees.
### Method
Data was collected from Glassdoor’s website through web scraping. A unique URL  was used that included filters on Glassdoor’s site, where search results were filtered for companies that had locations in the United States; had a rating of 3.5 and above; and were of the Information Technology sector. This URL provided about 20,000 search results. Using the Selenium library for Python, and with that URL, a script was ran that scraped through about 150 pages of search results and collected the necessary information for each variable. About 1,500 companies were scraped. After cleaning the data, removing the missing values and any duplicates, this figure was brought down to 991.
### Analysis
Before running machine algorithms on the data, the location and company size variables had to be numerically encoded. Midwest was encoded as 1, Northeast as 2, South as 3, and West as 4. Big was encoded as 1, Medium as 2, and Small as 3. The dataset was split into a training set and a test set, where 20% of the data would be for testing, and 80% would be for training. The Random Forest Regression algorithm was then used on the dataset to produce a model that would predict company ratings.
### Results
The model had a variance score of about 76%, which means that the predictor variables can explain 76% of the change that is happening with the company ratings. This suggests that location, company size, revenue, Glassdoor awards, other awards, and interview difficulty can likely predict a company’s ratings. The model also had a mean absolute error of about 24%, which is deemed acceptable, as it is closer to 0.
### Conclusion
The overall purpose of this report was to answer the question: Is there a trend in better rated tech companies across the United States, where some regions have better rated companies than others? From the analysis, it was found that there is a trend, as the model was able to explain a high percentage of the change in company ratings. Therefore, it can predict what a company’s rating would be if it were for example located in the west, with a big company size, and an average interview difficulty rating. In order for more robust model, it is recommended that a dataset with more records of at least 10,000 and more variables should be used to train the model and produce more accurate results. It may result in a lower error rate and better performance. 

### Appendix
- Web scraping script: https://github.com/conuma/INST414-Final/blob/master/glassdoor_scrape2.py 
- Data cleaning script: https://github.com/conuma/INST414-Final/blob/master/glassdoor_clean.py 
- Analysis – machine learning script: https://github.com/conuma/INST414-Final/blob/master/glassdoor_ml.py 
- Dataset: https://github.com/conuma/INST414-Final/blob/master/glassdoor4.csv 
- Cleaned Dataset: https://github.com/conuma/INST414-Final/blob/master/glassdoor_clean.csv 

