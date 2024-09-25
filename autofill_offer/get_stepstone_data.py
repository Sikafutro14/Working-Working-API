def cookie_popup(page):
    #Click the cookie accept button
    try:
        page.wait_for_selector('#ccmgt_explicit_accept')
        cookie_button = page.locator('#ccmgt_explicit_accept')
        
        if cookie_button.is_visible():
            cookie_button.click()
            print("Cookie pop-up accepted.")
        else:
            print("No cookie pop-up found.")

    except Exception as e:
        print(f"Error: {e}")

def get_offer_description(page):
    description = []
    try:
        page.wait_for_selector('[data-genesis-element="CARD_CONTENT"]')

        card_contents = page.locator('[data-genesis-element="CARD_CONTENT"] span')

        count = card_contents.count()

        for i in range(count):
            element = card_contents.nth(i)
            data_at = element.get_attribute("data-at")

            if "Neugierig auf das Gehalt für diesen Job?" in element.inner_text():
                break
            if data_at == "divider" or data_at == "apply-now-section":
                break

            if len(element.inner_text()) > 50:
                text = element.inner_text()
                description.append(text)
        return description[0],description[1:]

    except Exception as e:
        print(f"Error: {e}")
    
def get_stepstone_data(page):
    print(f"Import of {__name__} successful")
    #Get the Offer data
    cookie_popup(page)
    try:
        company_title = page.locator('//*[@id="JobAdContent"]//span[2]/span').inner_text() 
        job_title = page.locator('h1[data-at="header-job-title"]').inner_text()
        company_description, offer_description = get_offer_description(page)
        

        return [company_title, job_title, company_description , offer_description]

    except Exception as e:
        print(f"Error fetching offer informations: {e}")