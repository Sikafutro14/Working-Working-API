from playwright.sync_api import sync_playwright

from scrape_module.get_stepstone_data import get_stepstone_data
from scrape_module.get_indeed_data import get_indeed_data
from scrape_module.get_stellenanzeigen_data import get_stellenanzeigen_data

def get_content(plattform_name, url):
    print(f"Import of {__name__} successful")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        try:
            match plattform_name:
                    case "stepstone":
                        return get_stepstone_data(page)    
                    case "indeed":
                        return get_indeed_data(page)
                    case "stellenanzeigen":
                        return get_stellenanzeigen_data(page)
        except: 
            raise ValueError (f'No support for the website {plattform_name}')
        finally:
            browser.close()