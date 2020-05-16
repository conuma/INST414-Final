# -*- coding: utf-8 -*-
"""
Created on Thu May 14 21:56:06 2020

@author: cathe
"""

import pandas as pd
from bs4 import BeautifulSoup
import time
from random import randint
from warnings import warn
from IPython.core.display import clear_output
from selenium import webdriver
import re

# initialize variables for loop monitoring
start_time = time.time()
request = 0

# initialize page number variable
num = 1

# initialize the lists to make dataframe
comp_name = []
ratings = []
locations = []
company_size = []
revenue = []
glass_awards = []
other_awards = []
interview_diff = []
headquarters = []

us_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

headers = {'User-Agent': 'Chrome/81.0.4044.122'}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless') # use webdriver in headless mode
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)


try:
    while num < 1000:
        url = "https://www.glassdoor.com/Explore/Browse-Companies.htm?overall_rating_low=3.5&page="+str(num)+"&isHiringSurge=0&locId=1&locType=N&locName=United%20States&sector=10013"
        driver.get(url)
        time.sleep(20)
        html = driver.page_source
        # Monitor the requests
        request += 1
        elapsed_time = time.time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(request, request/elapsed_time))
        clear_output(wait=True)
        # Break the loop if the number of requests is greater than expected
        if request > 1000:
            warn('Number of requests was greater than expected.')
            break
        bs = BeautifulSoup(html,'lxml')
        
        # container
        #container = bs.find('div', {'class': {'col-md-8'}})
        containers = bs.find_all('section', {'data-test': {'employer-card-single'}})
        for container in containers:
            # company name
            company = container.find('h2', {'data-test': {'employer-short-name'}}).text
            comp_name.append(company)
            # rating
            rate = container.find('span', {'data-test': {'rating'}}).text
            ratings.append(rate)
            # locations
            comp_loc = container.find('span', {'data-test': {'employer-location'}})
            locations_us = []
            try:
                loc = comp_loc.find('a').get('href')
                loc_link = "https://www.glassdoor.com"+loc
                driver2 = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
                driver2.get(loc_link) # get request to link of office locations of a company
                time.sleep(randint(1, 4))
                html_loc = driver2.page_source # gets the html information
                bs_loc = BeautifulSoup(html_loc,'lxml') # parses the html
                locs = bs_loc.find_all('section', {'class': {'module'}})
                if len(locs) == 1:
                        p = locs[0].find_all('p', {'class': {'mb-0 mt-0'}})
                        for i in p:
                            txt = i.find('strong').get_text()
                            txt_split = txt.split(", ")
                            if txt_split[1] in us_states:
                                locations_us.append(txt_split[1])
                        locations.append(locations_us)
                else:
                    for i in locs:
                        cont = i.find('a').get('name')
                        if cont == "North America": # if location is in North America, then get the names of the locations and add it to list
                            us_locs = i.find_all('strong')
                            for i in us_locs:
                                us_loc_text = i.find('a').get_text()
                                us_loc_split = us_loc_text.split(", ")
                                locations_us.append(us_loc_split[1]) # only get the state
                    locations.append(locations_us)
            except AttributeError:
                loc_one = comp_loc.string
                locations.append(loc_one)
                
            # company overview
            try:
                lnk_container = container.find('div', {'class': {'col-12 my-0 mt-sm mt-sm-std order-5'}})
                lnk = lnk_container.find('a').get('href')
                overview_lnk = "https://www.glassdoor.com"+lnk
                driver3 = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
                driver3.get(overview_lnk)
                time.sleep(30)
                html_overview = driver3.page_source
                bs_overview = BeautifulSoup(html_overview,'lxml')
                infos = bs_overview.find_all('div', {'class': {'infoEntity'}})
                # scrape headquarters location
                head = infos[1].find('span').get_text()
                headquarters.append(head)
                # scrape size
                size = infos[2].find('span').get_text()
                company_size.append(size)
                # scrape revenue
                company_revenue = infos[len(infos)-1].find('span').get_text()
                revenue.append(company_revenue)
                # Glassdoor Award?
                basic = bs_overview.find('div', {'id': {'EmpBasicInfo'}})
                if basic.find(string=re.compile("Glassdoor Awards")):
                    glass_awards.append(1)
                else:
                    glass_awards.append(0)
                # Awards outside of Glassdoor?
                awards = bs_overview.find('div', {'id': {'Awards'}})
                if awards.find('ul'):
                    other_awards.append(1)
                else:
                    other_awards.append(0)          
                # scrape interview difficulty
                avg = bs_overview.find('div', {'class': {'difficultyLabel subtle'}}).get_text()
                interview_diff.append(avg)
            except:
                headquarters.append("NA")
                company_size.append("NA")
                revenue.append("NA")
                glass_awards.append("NA")
                other_awards.append("NA")
                interview_diff.append("NA")
                continue
        num = num + 1 # increment page number
    
    glassdoor_df = pd.DataFrame({'company': comp_name, 'rating': ratings,'location': locations, 'headquarters': headquarters, 'company_size': company_size, 
                                            'revenue': revenue, 'glassdoor_awards': glass_awards, 'other_awards': other_awards, 
                                            'interview_difficulty': interview_diff})
    print(glassdoor_df.info)
    print(glassdoor_df)
    glassdoor_df.to_csv("glassdoor3.csv")
    driver.quit()
    
except Exception as e:
    print(e)
    glassdoor2_df = pd.DataFrame.from_dict({'company': comp_name, 'rating': ratings,'location': locations, 'headquarters': headquarters, 'company_size': company_size, 
                                            'revenue': revenue, 'glassdoor_awards': glass_awards, 'other_awards': other_awards, 
                                            'interview_difficulty': interview_diff}, orient='index')
    print(glassdoor2_df.info)
    print(glassdoor2_df)
    glassdoor2_df.transpose().to_csv("glassdoor4.csv")
    driver.quit()