import requests
from bs4 import BeautifulSoup
from typing import List
from random import shuffle

class Crawler:
    '''
    더미 데이터 생성을 위해 회사 이름 또는 회사 로고 URL을 크롤링한다.
    '''

    def __init__(self, length: int) -> None:
        '''
        Parameters
        ----------
        length: int
            크롤링 후 반환할 데이터의 갯수
        '''
        self.__length = length
    
    def get_length(self) -> int:
        return self.__length

    def set_length(self, length: int) -> None:
        self.__length = length


    def crawl_names(self) -> List[str]:
        '''
        위키피디아에서 회사 목록 크롤링
        먼저 대학교들을 제외한 후 이름에서 다음을 제거한다.
        1. ()안의 문자열
        2. 양 끝의 공백
        '''
        url = 'https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EA%B8%B0%EC%97%85_%EB%AA%A9%EB%A1%9D'
        parser = 'html.parser'
        html = requests.get(url=url).text
        soup = BeautifulSoup(markup=html, features=parser)
        data = soup.find(name='div', attrs={'class': 'mw-page-container-inner'}) \
            .find(name='div', attrs={'class': 'mw-content-container'}) \
            .find(name='div', attrs={'id': 'bodyContent'}) \
            .find(name='div', attrs={'id': 'mw-content-text'}) \
            .find(name='div', attrs={'class': 'mw-parser-output'}) \
            .find(name='ul', attrs=None) \
            .find_all(name="li", attrs=None)
        result = []

        for d in data:
            t: str = d.text
            
            if '대학교' in t:
                continue

            if '(' in t:
                t = t[:t.index('(')]
            result.append(t.strip())
        shuffle(result)

        return result[:self.__length]


    def crawl_logo_urls(self) -> List[str]:
        l = ((self.__length)//32) + 1 # 한 페이지에 32개씩 뜸
        result = []
        for page in range(1, l + 1):
            url = f'https://worldvectorlogo.com/most-downloaded/{page}'
            parser = 'html.parser'
            html = requests.get(url=url).text
            soup = BeautifulSoup(markup=html, features=parser)
            grids = \
                soup.find(name='div', attrs={'class': 'frame'}) \
                .find(name='main', attrs={'class': 'row expand'}) \
                .find(name='div', attrs={'class': 'wrapper'}) \
                .find(name='div', attrs={'class': 'logos'}) \
                .find_all(name='div', attrs={'class': 'grid__col'})
            
            logo_urls = [grid.find(name='a').get_attribute_list(key='href')[0] for grid in grids]
            for logo_url in logo_urls:
                logo_html = requests.get(url=logo_url).text
                logo_soup = BeautifulSoup(markup=logo_html, features=parser)

                svg_image_url = \
                    logo_soup.find(name='img', attrs={'class': 'larger'}) \
                        .get_attribute_list(key='src')[0]

                result.append(svg_image_url)
        shuffle(result)

        return result[:self.__length]
