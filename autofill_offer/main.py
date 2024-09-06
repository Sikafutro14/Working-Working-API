#NOT THE CURRENT VERSION
def main(input):
    input_url = input.split(".")
    plattform_name = input_url[1]

    try:
        match plattform_name:
            case "stepstone":
                pass
            case "indeed":
                pass
            case "stellenanzeigen":
                pass
    except: raise ValueError (f'No support for {plattform_name}')
#testcases
testcase1 = r"https://www.steqpstone.de/stellenangebote--Linux-Virtualization-Developer-w-m-d-vGPU-QEMU-KVM-bundesweit-Home-Office-Berlin-Karlsruhe-IONOS--11055827-inline.html?rltr=12_12_25_seorl_s_0_0_0_0_0_0" 
testcase2 = r"https://www.stellenanzeigen.de/suche/?fulltext=Python-Entwickler%2Fin&jobId=13160713"
testcase3 = r"https://de.indeed.com/jobs?q=python&l=&from=searchOnHP&vjk=eaebb32418b14216&advn=7842752898364246"
main(testcase1)

