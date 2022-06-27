import requests
from bs4 import BeautifulSoup

def Scraping_NIKKEI():

    url = "https://www.nikkei.com/markets/ranking/page/?bd=disclose" # ���{�o�ϐV�� �K�X�J�������L���O

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find('table') # rank_table
    thead = table.find('thead')  
    tbody = table.find('tbody') 

    for target in tbody.find_all('div'):
        target.decompose()

    for target in tbody.find_all('p'):
        target.decompose()

    for target in tbody.find_all('h6'):
        target.decompose()

    ths = thead.tr.find_all('th')
    trs = tbody.find_all('tr') 

    result = []
    temp = []  

    for th in ths:  # thead -> tr����th�^�O��T��
        t = th.text
        temp.append(t.strip())  # th�^�O�̃e�L�X�g��ۑ�

    result.append(temp) 

    for tr in trs:
        temp = []
        for td in tr.find_all('td'):  # tr�^�O����td�^�O��T��
            t = td.text
            temp.append(t.strip())  # td�^�O�̃e�L�X�g��ۑ�

    result.append(temp)

    return result

    # �o��
    for temp in result:
        print(','.join(temp))  # �J���}�i,�j�ŗ���������ĕ\��


def Scraping_NIKKEI():
