from get_content import get_content
def get_offer_information(input):
    try:
        input_url = input.split(".")
        plattform_name = input_url[1]
        offer_information = get_content(plattform_name, input)
        if offer_information:
            print(offer_information)
        
    except Exception as e: 
        raise ValueError(f'INVALID INPUT: {input_url} Error:{e}')

#testcases
testcase1 = r"https://www.stepstone.de/stellenangebote--Linux-Virtualization-Developer-w-m-d-vGPU-QEMU-KVM-bundesweit-Home-Office-Berlin-Karlsruhe-IONOS--11055827-inline.html?rltr=12_12_25_seorl_s_0_0_0_0_0_0" 
testcase2 = r"https://www.stepstone.de/stellenangebote--Bauleiter-m-w-d-fuer-den-Strassenbau-mit-Zukunftsperspektive-technische-Leitung-Geschaeftsfuehrung-Berlin-HTF-Hoch-Tiefbau-in-Friedrichshain-GmbH--11539905-inline.html?rltr=1_1_25_seorl_m_0_0_0_0_0_0"
testcase3 = r"https://www.stellenanzeigen.de/job/software-entwickler-python-m-w-d-erlangen-12805300/"
testcase4 = r"https://de.indeed.com/jobs?q=python&l=&from=searchOnHP&vjk=eaebb32418b14216&advn=7842752898364246"

get_offer_information(testcase1)

