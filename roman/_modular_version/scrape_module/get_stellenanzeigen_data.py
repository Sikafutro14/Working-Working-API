def cookie_popup(page):
    #Click the cookie accept button
    try:
        page.wait_for_selector('#cmpwelcomebtnyes > a')
        cookie_button = page.locator('#cmpwelcomebtnyes > a')
        
        if cookie_button.is_visible():
            cookie_button.click()
            print("Cookie pop-up accepted.")
        else:
            print("No cookie pop-up found.")

    except Exception as e:
        print(f"Error: {e}")

def get_offer_description(page):
    #get the offer_description
    offer_description = []
    """try:
        page.wait_for_selector('#JobAdContent > div > div > div > div > div > div > div > div.job-ad-display-e6cidt > div:nth-child(1) > div > article > div > span > ul')

        offer_description_list = page.locator('#JobAdContent > div > div > div > div > div > div > div > div.job-ad-display-e6cidt > div:nth-child(1) > div > article > div > span > ul')
        li_elements = offer_description_list.locator('li') 
        li_texts = li_elements.all_inner_texts()
         
        for text in li_texts:
            offer_description.append(text)

    except Exception as e:
        print(f"Error fetching offer description: {e}")
    
    return offer_description"""
    

def get_stellenanzeigen_data(page):
    print(f"Import of {__name__} successful")
    #Get the Offer data
    cookie_popup(page)
    
    try:
        company_title = page.locator('//*[@id="job-ad-regular-header"]/div/div[1]/div[3]/a').inner_text()
        job_title = page.locator('//*[@id="job-ad-regular-header"]/div/div[1]/h1').inner_text()
        page.wait_for_selector('#wrapper > article > p')
        company_description = page.locator('').inner_text()
        #offer_description = get_offer_description(page)
        
        print(company_title, job_title, company_description)
        #return [company_title, job_title, company_description, offer_description]

    except Exception as e:
        print(f"Error fetching offer informations: {e}")