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

def get_iframe_url(page):
    """  
    try:
        frames = page.frames

        if len(frames) > 1:
            first_iframe = frames[1]
            iframe_url = first_iframe.url
            print(f"First iframe URL: {iframe_url}")
            return iframe_url
        else:
            print("No iframes found on the page.")
            return None
    
    except Exception as e:
        print(f"Error fetching iframe URL: {e}")
    try:
    
        frames = page.frames()
        iframe_url = frames[1].url()
        print(f"Iframe URL: {iframe_url}")
    except Exception as e:
        print(f"Error fetching offer informations: {e}")
    """

    try:
        # Wait for the elements to be visible
        page.wait_for_selector('[data-genesis-element="CARD_CONTENT"]')

        # Target all the elements matching the locator
        card_contents = page.locator('[data-genesis-element="CARD_CONTENT"]')

        # Get the count of matching elements
        count = card_contents.count()
        print(f"Number of matching CARD_CONTENT elements: {count}")

        # Loop through each matching element and print its inner text
        for i in range(count):
            text = card_contents.nth(i).inner_text()
            print(f"Text in CARD_CONTENT #{i + 1}: {text}")

    except Exception as e:
        print(f"Error: {e}")

      
        print(f"Error: {e}")
def get_stellenanzeigen_data(page):
    print(f"Import of {__name__} successful")
    #Get the Offer data
    cookie_popup(page)
    
    try:
        company_title = page.locator('//*[@id="job-ad-regular-header"]/div/div[1]/div[3]/a').inner_text()
        job_title = page.locator('//*[@id="job-ad-regular-header"]/div/div[1]/h1').inner_text()
        
    
        iframe = get_iframe_url(page)


        #print(company_title, job_title, company_description)
        #return [company_title, job_title, company_description, offer_description]

    except Exception as e:
        print(f"Error fetching offer informations: {e}")