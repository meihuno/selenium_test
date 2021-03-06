from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common import action_chains
import chromedriver_binary
import pprint as pp
import json

class TBTPdfDownLoader():

    def __init__(self, date="2022-06-13"):
        self.browser = webdriver.Chrome()
        self.date = date
        self.target_url = 'https://docs.wto.org/dol2fe/Pages/FE_Browse/FE_B_002.aspx'

        # self.target_url = 'https://docs.wto.org/dol2fe/Pages/FE_Search/FE_S_S006.aspx?Language=ENGLISH&SourcePage=FE_S_S002&Context=RD&PostingDateFrom=17/06/2022&PostingDateTo=19/06/2022&IsEnglishSelected=True&IsFrenchSelected=True&IsSpanishSelected=True&IsAllLanguageSelected=True&FullTextHash=371857150&SearchPage=FE_B_002&TopicId=0&languageUIChanged=true#'
        self.doc_dict = {}
        self.set_chrome_options()
        
    def set_chrome_options(self):
    
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
            "download.default_directory": "/Users/sugihara/void/toy/python/translate/seleniumtest/seleniumtest/temp", #Change default directory for downloads
            "download.prompt_for_download": False, #To auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })
        # self.driver = webdriver.Chrome(options=options)
        self.browser = webdriver.Chrome(options=options)

    def _dict_conbine(self, doc_dict, rdict):
        for doc_num, doclist in rdict.items():
            if doc_num in doc_dict:
                if doc_num == len(doclist):
                    doc_dict[num]['doclist'] = doclist
        return doc_dict
    
    def ret_content_list_dict(self):
        rdict = {}
        doc_dict = {}
        clist = self.browser.find_elements(By.ID, 'daily_contents_list')
        for dcon in clist:
            print(["dcon", dcon])
            doc_name_list = dcon.find_elements(By.CLASS_NAME, 'title_area')
            d_count = 0
            for dc, doc_name1 in enumerate(doc_name_list):
                doc_name = doc_name1.find_element(By.TAG_NAME, 'h4').text
                num = doc_name1.find_element(By.TAG_NAME, 'strong').text
                doc_dict[dc] = {'category': doc_name, 'num': num}
            
            ul_list = dcon.find_elements(By.CSS_SELECTOR, 'ul.list')
            for uc, ullist in enumerate(ul_list):
                # print(["ullist", ullist.text])
                if not uc in rdict:
                    rdict[uc] = []
                li_list = ullist.find_elements(By.TAG_NAME, 'li')
                for li in li_list:
                    rdict[uc].append(li.text)

        pp.pprint(doc_dict)
        pp.pprint(rdict)
        rdict1 = self._dict_conbine(doc_dict, rdict)
        return rdict1

    def save_json(self):
        if len(self.doc_dict) > 0:
            with open('./temp/doc_dict.json', 'w') as f:
                json.dump(self.doc_dict, f, indent=4)


    def open_window(self, wlink):
        wait = WebDriverWait(self.browser, 15)
        wlink.click()
        wait.until(lambda d: len(self.browser.window_handles) > 1)
        self.browser.switch_to.window(self.browser.window_handles[1])
        wait.until(EC.presence_of_all_elements_located)
        current_url = self.browser.current_url
        # sleep(5)
        # print('waiting 5')
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        # sleep(5)
        # print('waiting 10')
        return current_url
        
    def link_loop_test(self, set_dict, count):
        # html.t-ff.t-ff99 body form#aspnetForm div#ctl00_PanelMaster table tbody tr td div#body div#contentPlaceHolder table tbody tr td div#searchResults table#ctl00_MainPlaceHolder_tableFooter tbody tr td a#ctl00_MainPlaceHolder_lnkNext
        wait = WebDriverWait(self.browser, 15)
        wait.until(EC.presence_of_all_elements_located)
        print(["in", count])
        sleep(5)

        divs = self.browser.find_elements(By.CLASS_NAME, 'hitContainer')
        for div in divs:
            symbol = div.find_element(By.CLASS_NAME, 'hitSymbol')
            symbolstr = symbol.text
            symbolstr = symbolstr.replace(' ', '')
            wlinks = div.find_elements(By.CLASS_NAME, 'FECatalogueSymbolPreviewCss')
            if not symbolstr in set_dict:
                set_dict[symbolstr] = []

            if len(wlinks) > 0:
                wlink = wlinks[0]
                # curl = self.open_window(wlink)
                # set_dict[symbolstr].append(curl)
                set_dict[symbolstr].append("link")
            else:
                set_dict[symbolstr].append("no link")
                
        next_links = self.browser.find_elements(By.ID, 'ctl00_MainPlaceHolder_lnkNext')
        if len(next_links) > 0:
            next_link = None
            next_link = next_links[0]
            # print([next_link.get_attribute('innerHTML'), next_link.get_attribute('disabled')])
            print([next_link.text, next_link.is_enabled(), next_link])
            if next_link.get_attribute('disabled') is None:
                next_link.click()
                count += 1
                self.link_loop_test(set_dict, count)

    def get_pdf2(self):

        self.browser.implicitly_wait(10)
        self.browser.get(self.target_url)

        print("wait")
        wait = WebDriverWait(self.browser, 15)
        wait.until(EC.presence_of_all_elements_located)
        
        print("start")
        
        # try:
        if 1 == 1:
            wait.until(EC.presence_of_all_elements_located)
            div = self.browser.find_element(By.ID, 'ctl00_MainPlaceHolder_DatePickerWUC1_txtCalendar_wrapper')
            # texts = div.find_element(By.ID, 'ctl00_MainPlaceHolder_DatePickerWUC1_txtCalendar')
            # ctl00_MainPlaceHolder_DatePickerWUC1_txtCalendar_dateInput

            texts = div.find_element(By.ID, 'ctl00_MainPlaceHolder_DatePickerWUC1_txtCalendar_dateInput')
            print("elem")
            print([texts])
            # print([texts.get_attribute('innerHTML')])
            # div.click()
            print("gogo")
            texts.click()
            texts.clear()
            texts.send_keys('07/03/2022')

            div = self.browser.find_element(By.ID, 'ctl00_MainPlaceHolder_DatePickerWUC2_txtCalendar_wrapper')
            texts = div.find_element(By.ID, 'ctl00_MainPlaceHolder_DatePickerWUC2_txtCalendar_dateInput')
            print("elem")
            print([texts])
            # print([texts.get_attribute('innerHTML')])
            # div.click()
            print("gogo")
            texts.click()
            texts.clear()
            texts.send_keys('07/03/2022')
            print("gogo1")
            
            check1 = self.browser.find_element(By.ID, 'ctl00_MainPlaceHolder_chk009')
            print(check1)
            print(check1.is_selected())
            check1.click()
            print(check1.is_selected())
            """
            """
            
            check2 = self.browser.find_element(By.ID, 'ctl00_MainPlaceHolder_chk0010')
            print(check2)
            print(check2.is_selected())
            check2.click()
            print(check2.is_selected())
            
            # print("gogo")
            # #ctl00_MainPlaceHolder_chk0010
            # #ctl00_MainPlaceHolder_chk0010

            # check1 = self.browser.find_element(By.ID, 'ctl00_MainPlaceHolder_chk0010')
            # check1.click()
            
            sbutton = self.browser.find_element(By.ID, 'ctl00_MainPlaceHolder_btn011')
            sbutton.click()
            wait.until(EC.presence_of_all_elements_located)

            count = 0
            set_dict = {}
            self.link_loop_test(set_dict, count)

            pp.pprint(len(set_dict))
            for k,v in set_dict.items():
                print([k,v])
            
            # dbutton = self.browser.find_element(By.ID, 'ctl00_MainPlaceHolder_btn012')
            # dbutton.click()
            # search
            #ctl00_MainPlaceHolder_btn011

            # download
            #html.t-ff.t-ff99 body form#aspnetForm div#ctl00_PanelMaster table tbody tr td div#body div#contentPlaceHolder table tbody tr td div#ctl00_MainPlaceHolder_pnlDoSearch div.FEContentClass table tbody tr td input#ctl00_MainPlaceHolder_btn012.SearchClearButton
            ##ctl00_MainPlaceHolder_btn012
            
            # #ctl00_MainPlaceHolder_DatePickerWUC1_txtCalendar_wrapper
            # list1 = self.browser.find_element(By.ID, 'ctl00_MainPlaceHolder_DatePickerWUC1_txtCalendar')
            # print("send")
            # print(list1)

            # html.t-ff.t-ff99 body form#aspnetForm div#ctl00_PanelMaster table tbody tr td div#body div#contentPlaceHolder table tbody tr td div#ctl00_MainPlaceHolder_pnlDoSearch div.FEContentClass table tbody tr td input#ctl00_MainPlaceHolder_btn012.SearchClearButton
            
            # list1[0].send_keys(self.date)
            # sleep(3)
            # texts.clear()
            # texts.send_keys(self.date)
        else:
        #except Exception as e:
            print(str(e))
            self.browser.close()
            print("exit")

            

    
    def get_pdf(self):

        self.browser.implicitly_wait(10)
        self.browser.get(self.target_url)
        
        wait = WebDriverWait(self.browser, 15)
        wait.until(EC.presence_of_all_elements_located)
        
        download_status = "start"
        
        try:
            
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul#daily_data_category_list')))
            
            texts = self.browser.find_element(By.ID, 'datapicker_searchdate')
            texts.send_keys(self.date)
            sleep(3)
            texts.clear()
            texts.send_keys(self.date)
            
            sbutton = self.browser.find_element(By.CLASS_NAME, 'btn_search')
            sbutton.click()
            sleep(10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul#daily_data_category_list li a span')))
            print("wait over")
            span = self.browser.find_element(By.CSS_SELECTOR, 'ul#daily_data_category_list li a span')
            snum = span.text
            
            if int(snum) > 1000:
                buton_list = self.browser.find_elements(By.CLASS_NAME, 'btn_download')
                buton_list[1].click()
                wait.until(EC.alert_is_present())
                print("wait over2")
                # POST???jquery.fileDownload???????????????callback?????????alert???OK???????????????????????????????????????????????????????????????????????????????????????20????????????
                sleep(20)
                alert = self.browser.switch_to.alert
                print("wait over3")
                if alert.text == '???????????? ??????':
                    download_status = 'success'
                    print(["Alert text Success", alert.text])
                elif alert_text == '???????????? ??????':
                    download_status = 'failure'
                    print(["Alert text failure", alert.text])
                alert.accept()
                print("OK0")
            elif int(snum) == 0:
                print("OK1")
                download_status = 'not found'
            else:
                download_status = 'error'
                print("OK2")
                
            download_status = 'success'
            ## ????????????????????????????????????
            if download_status == 'success':
                print("IN")
                self.doc_dict = self.ret_content_list_dict()
            
            self.browser.close()
        
        except Exception as e:
            print(e)
            self.browser.close()
            print("exit")


            
if __name__ == "__main__":
    box = TBTPdfDownLoader()
    box.get_pdf2()
    # box.save_json()
