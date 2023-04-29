import pandas as pd

from crawler import Crawler

from random import randint

from datetime import datetime
from datetime import timedelta

import sys, os
sys.path.append(
    os.path.dirname(
        os.path.abspath(
            os.path.dirname(__file__)))) 

class Generator:
    '''
    특정 컬럼에 대한 더미 데이터를 생성하는 클래스.
    컬럼은 코드 값으로 주어지며 이는 상수로 선언되어 있다.
    '''

    ALL = 0
    NAME = 1
    LOGO_IMAGE_URL = 2
    TITLE = 3
    POSTER_URL = 4
    CONTENT = 5
    JOB = 6
    LOCATION = 7
    SCALE = 8
    IS_REGULAR = 9
    EXPERIENCED_YEARS = 10
    SALARY = 11
    DATE = 12
    COLUMNS = {
        NAME: 'company_name',                    # 회사명
        LOGO_IMAGE_URL: 'company_image_url',     # 회사 로고 이미지 URL
        TITLE: 'title',                          # 공고 제목
        POSTER_URL: 'poster_url',                # 공고 포스터 이미지 URL
        CONTENT: 'content',                      # 공고 내용
        JOB: 'job',                              # 직무
        LOCATION: 'location',                    # 지역
        SCALE: 'company_scale',                  # 기업 규모
        IS_REGULAR: 'regular',                   # 정규직, 비정규직
        EXPERIENCED_YEARS: 'experienced_years',  # 경력 0, 1, ... / 0이면 신입
        SALARY: 'salary',                        # 급여
        DATE: None
    }
    '''
    Constants
    ---------
    ALL: int
        모든 컬럼에 대한 더미 데이터를 얻기 위한 코드
    나머지 코드 값: int
        그 상수 이름에 대응되는 컬럼에 대한 더미 데이터를 얻기 위한 코드
    COLUMNS dict[int, str]:
        컬럼명을 코드로 접근하기 위한 딕셔너리
    '''


    # CORPORATE = 'COPR' # 대기업
    # MIDSIZE = 'MID' # 중견기업
    # SMES = 'SMEs' # 중소기업
    # SMALL = 'SMALL' # 소기업
    # START_UP = 'STUP' #스타트업'
    CORPORATE =  '대기업'
    MIDSIZE = '중견기업'
    SMES = '중소기업'
    SMALL = '소기업'
    START_UP = '스타트업'
    SCALE_DOMAIN = (
        CORPORATE,
        MIDSIZE,
        SMES,
        SMALL,
        START_UP
    )
    '''
    Constants
    ---------
    기업 규모를 나타내는 상수
    더이상의 자세한 설명은 생략한다.
    '''

    PLANING = '전략기획'
    MARKETING = '마케팅'
    FINANCE = '재무'
    LEGAL = '법무'
    HR = '인사'
    IT = 'IT'
    DA = '데이터 분석'
    DESIGN = '디자인'
    SALES = '영업'
    TRADE = '무역'
    PROCUREMENT = '조달'
    LOGISTICS = '물류'
    EDUCATION = '교육'
    MEDIA = '미디어'
    INSURANCE = '보험'
    CONSTRUCTION = '건설'
    MANUFACTURING = '생산'
    RND = '연구개발(R&D)'
    JOB_DOMAIN = (
        PLANING,
        MARKETING,
        FINANCE,
        LEGAL,
        HR,
        IT,
        DA,
        DESIGN,
        SALES,
        TRADE,
        PROCUREMENT,
        LOGISTICS,
        EDUCATION,
        MEDIA,
        INSURANCE,
        CONSTRUCTION,
        MANUFACTURING,
        RND
    )
    '''
    Constants
    ---------
    직무를 나타내는 상수
    '''

    SEUL = '서울'
    JEJU = '제주'
    GWJU = '광주'
    DAGU = '대구'
    DAJN = '대전'
    BUSN = '부산'
    ULSN = '울산'
    INCN = '인천'
    GAWN = '강원'
    GNGI = '경기'
    GYNM = '경남'
    GYBK = '경북'
    JONM = '전남'
    JOBK = '전북'
    CHNM = '충남'
    CHBK = '충북'
    LOCATION_DOMAIN = (
        SEUL,
        JEJU,
        GWJU,
        DAGU,
        DAJN,
        BUSN,
        ULSN,
        INCN,
        GAWN,
        GNGI,
        GYNM,
        GYBK,
        JONM,
        JOBK,
        CHNM,
        CHBK
    )
    '''
    Constants
    ---------
    1개의 특별시(서울),
    1개의 특별자치도(제주),
    6개의 광역시(광주, 대구, 대전, 부산, 울산, 인천)
    8개의 도(강원, 경기, 경남, 경북, 전남, 전북, 충남, 충북)
    '''

    JSON = 'json'
    CSV = 'csv'
    EXCEL = 'xlsx'
    '''
    Constants
    ---------
    JSON: str
    CSV: str
    EXCEL: str
        저장할 확장자명
    '''


    MIN_LENGTH = 10
    MAX_LENGTH = 500
    '''
    Constants
    ---------
    MIN_LENGTH: int
        데이터를 생성할 수 있는 최소 개수
        default: 10
    MAX_LENGTH: int
        데이터를 생성할 수 있는 최대 개수
        default: 500
    '''
    
    def __init__(self, length=50, code=ALL, format=JSON) -> None:
        '''
        Parameters
        ----------
        generate: function
            주어진 코드 값에 대응되는 컬럼의 데이터를 얻는다.
            default: 모든 데이터를 반환한다.
        length: int
            생성할 데이터 수
            default: 50
        code: int
            데이터를 생성할 컬럼의 코드
            default: ALL
        methods: dict[int, Callable]
            key: 데이터를 생성할 컬럼의 코드
            value: 코드에 대응되는 데이터를 생성하는 함수
        '''
        if self.MAX_LENGTH < length:
            self.__length = self.MAX_LENGTH
        elif length < 0:
            self.__length = self.MIN_LENGTH
        else:
            self.__length = length
        self.__code = code
        self.__format = format

        self.__path=f'..\\data.{self.__format}'
        #self.__path=f'D:\\Kirisame\\\Study\\Extra\\Kakao-Cloud-School\\Final-Project\\Data-Generator\\data.{self.__format}'
        self.__data = None
        self.__METHOD_DICT = {
            self.ALL: self.__generate_all_data,
            self.NAME: self.__generate_name_data,
            self.LOGO_IMAGE_URL: self.__generate_logo_image_url_data,
            self.TITLE: self.__generate_title_data,
            self.POSTER_URL: self.__genarate_poster_url_data,
            self.CONTENT: self.__generate_content_data,
            self.JOB: self.__generate_job_data,
            self.LOCATION: self.__generate_location_data,
            self.SCALE: self.__generate_scale_data,
            self.IS_REGULAR: self.__generate_is_regular_data,
            self.EXPERIENCED_YEARS: self.__generate_experienced_years,
            self.SALARY: self.__generate_salary_data,
            self.DATE: self.__generate_date_data
        }
        self.generate = self.__METHOD_DICT[self.__code]
        self.__crawler = Crawler(length=self.__length)
        '''
        Fields
        ------
        __length: int
            생성할 데이터 수
            default: DEFAULT_SIZE
        __code: int
            데이터를 생성할 컬럼의 코드
            default: ALL
        __format: str
            데이터를 저장할 형식
            default: .json
        __data: DataFrame
            생성된 데이터
        __METHOD_DICT: dict[int, Callable]
            key: 데이터를 생성할 컬럼의 코드
            value: 코드에 대응되는 데이터를 생성하는 함수
        generate: Callable
            주어진 코드 값에 대응되는 컬럼의 데이터를 얻는다.
            default: __generate_all_data
        __crawler: Crawler
            length: 크롤링할 데이터 수
        '''

    def __str__(self):
        return f'{self.__length}_of_{self.generate}.{self.__format}'

    def __validate(self) -> bool:
        '''
        Parameters
        ----------
        모든 필드 값이 유효한지 검사한다.
        return: 모든 필드 값이 유효하면 True, 아니면 False
        '''
        data_is_valid = isinstance(self.__data, pd.DataFrame)
        length_is_valid = isinstance(self.__length, int) and self.__length > 0
        code_is_valid = isinstance(self.__code, int) and self.__code in self.COLUMNS.keys()
        generate_is_valid = callable(self.generate) and self.generate in (self.__METHOD_DICT.values())
        crawler_is_valid = isinstance(self.__crawler, Crawler) and self.__crawler.get_length() == self.__length
        format_is_valid = isinstance(self.__format, str) and self.__format in (self.JSON, self.CSV, self.EXCEL)
        if data_is_valid \
        and length_is_valid \
        and code_is_valid \
        and generate_is_valid \
        and crawler_is_valid \
        and format_is_valid:
            method_dict_is_valid = True
            for key in self.__METHOD_DICT.keys():
                if isinstance(key, int):
                    if not callable(self.methods(key)):
                        method_dict_is_valid = False
                        break
                else:
                    method_dict_is_valid = False
                    break

            return method_dict_is_valid
        else:
            return False


    def get_data(self) -> pd.DataFrame: 
        return self.__data


    def __generate_all_data(self):
        data_list = []
        for col in list(self.COLUMNS.keys()):
            self.__METHOD_DICT[col]()
            data_list.append(self.__data)

        data = pd.concat(objs=data_list, axis=1, ignore_index=False)
        print(data)
        for i in data.index:
            name = data.loc[i, self.COLUMNS[self.NAME]]
            job = data.loc[i, self.COLUMNS[self.JOB]]
            
            data.loc[i, self.COLUMNS[self.TITLE]] \
                = f'{name} {job} {data.loc[i, self.COLUMNS[self.TITLE]]}'
            
            data.loc[i, self.COLUMNS[self.CONTENT]] \
                = f'{name}에서 {job} 업무를 아는 {data.loc[i, self.COLUMNS[self.CONTENT]]}'

        self.__data = data

    

    def __generate_name_data(self):
        def __generate_character() -> str:
            '''
            랜덤으로 한 글자를 리턴한다.
            초성, 중성, 종성 리스트를 유니코드 규칙에 따라 결합하며,
            받침은 없거나 단자음으로 생성한다.
            '''
            # 초성 리스트
            initial_sound_indices= [0, 2, 3, 5, 6, 7, 9, 11, 12, 14, 15, 16, 17, 18]
            
            # 중성 리스트
            medial_sound_indices = [0, 1, 4, 5, 6, 8, 12, 13, 18, 20]
            
            # 종성 리스트
            final_sound_indices = [0, 1, 4, 7, 8, 16, 17, 19, 21]
            
            # 입력된 자음과 모음의 인덱스를 구한다
            consonant_index = initial_sound_indices[randint(0, len(initial_sound_indices) - 1)]
            vowel_index = medial_sound_indices[randint(0, len(medial_sound_indices) - 1)]
            #syllable_final_sound_index = final_sound_indices[randint(1, len(final_sound_indices) - 1) if randint(1, 10) >= 7 else 0]
            syllable_final_sound_index = final_sound_indices[0] # 받침 안 들어가게 함

            # 초성 + 중성 + 종성으로 조합하여 문자열을 만들고 반환한다
            return chr(0xAC00 + (consonant_index * 21 * 28) + (vowel_index * 28) + syllable_final_sound_index)
        
        column_name = self.COLUMNS[self.NAME]
        name_data = set()
        while len(name_data) < self.__length:
            characters = randint(2, 4)
            name = ''.join([__generate_character() for j in range(characters)])
            name_data.add(name)

        data = pd.DataFrame(
            data={
                column_name: list(name_data)
            }
        )
        self.__data = data

        # return pd.DataFrame(data=data)


    def __generate_logo_image_url_data(self):
        column_name = self.COLUMNS[self.LOGO_IMAGE_URL]
        crawled_data = self.__crawler.crawl_logo_urls()
        data = pd.DataFrame(
            data={
                column_name: crawled_data
            }
        )
        self.__data = data

        # return pd.DataFrame(data=data)


    def __generate_title_data(self):
        column_name = self.COLUMNS[self.TITLE]
        
        if self.__code != self.ALL:
            names = self.__generate_name_data()[self.COLUMNS[self.NAME]]
            jobs = self.__generate_job_data()[self.COLUMNS[self.JOB]].to_list()
            title_data = [f'{name} {job}부문 채용' for name, job in zip(names, jobs)]
            data = pd.DataFrame(
                data={
                    column_name: title_data
                }
            )
        else:
            title_data = [f'부문 채용' for _ in range(self.__length)]
            data = pd.DataFrame(
                data={
                    column_name: title_data
                }
            )
        self.__data = data


        # return pd.DataFrame(data=data)


    def __genarate_poster_url_data(self):
        column_name = self.COLUMNS[self.POSTER_URL]

        f = open('.\\posters\\urls.txt')
        urls = [text.strip() for text in f]
        f.close()

        l = len(urls)
        poster_url_data = [urls[randint(0, l - 1)] for _ in range(self.__length)]

        data = pd.DataFrame(
            data={
                column_name: poster_url_data
            }
        )
        self.__data = data

        # return pd.DataFrame(data=data)


    def __generate_content_data(self):
        column_name = self.COLUMNS[self.CONTENT]

        if self.__code != self.ALL:
            names = self.__generate_name_data()[self.COLUMNS[self.NAME]]
            jobs = self.__generate_job_data()[self.COLUMNS[self.JOB]].to_list()
            content_data = []
            for name, job in zip(names, jobs):
                content = f'{name}에서 {job} 직무 수행 인재 채용 중'
                content_data.append(content)

            data = pd.DataFrame(
                data={
                    column_name: content_data
                }
            )
        else:
            content_data = ['직무 수행 인재 채용 중' for _ in range(self.__length)]
            data = pd.DataFrame(
                data={
                    column_name: content_data
                }
            )
        self.__data = data
        
        # return pd.DataFrame(data=data)


    def __generate_job_data(self):
        column_name = self.COLUMNS[self.JOB]
        jobs = self.JOB_DOMAIN
        jobs_length = len(jobs)
        data = pd.DataFrame(
            data={
                column_name: [jobs[randint(0, jobs_length - 1)] for _ in range(self.__length)]
            }
        )
        self.__data = data

        # return pd.DataFrame(data=data)


    def __generate_location_data(self):
        column_name = self.COLUMNS[self.LOCATION]
        locations = self.LOCATION_DOMAIN
        locations_length = len(locations)
        data = pd.DataFrame(
            data={
                column_name: [locations[randint(0, locations_length - 1)] for _ in range(self.__length)]
            }
        )
        self.__data = data

        # return pd.DataFrame(data=data)
    

    def __generate_scale_data(self):
        column_name = self.COLUMNS[self.SCALE]
        scales = self.SCALE_DOMAIN
        scales_length = len(scales)
        data = pd.DataFrame(
            data={
                column_name: [scales[randint(0, scales_length - 1)] for _ in range(self.__length)]
            }
        )
        self.__data = data
        # return pd.DataFrame(data=data)


    def __generate_is_regular_data(self):
        column_name = self.COLUMNS[self.IS_REGULAR]
        data = pd.DataFrame(
            data={
                column_name: [bool(randint(0, 1))  for _ in range(self.__length)]
            }
        )
        self.__data = data

        # return pd.DataFrame(data=data)


    def __generate_experienced_years(self):
        '''
        신입 아님 경력
        '''
        column_name = self.COLUMNS[self.EXPERIENCED_YEARS]
        data = pd.DataFrame(
            data={
                #column_name: [randint(0, 5) for _ in range(self.__length)]
                column_name: [bool(randint(0, 1)) for _ in range(self.__length)]
            }
        )
        self.__data = data

        # return pd.DataFrame(data=data)

    
    def __generate_salary_data(self):
        '''
        단위는 만 원
        초봉이므로 3000 ~ 6000 사이의 값으로 책정한다.
        근데이제 100 단위인
        '''
        column_name = self.COLUMNS[self.SALARY]
        data = pd.DataFrame(
            data={
                column_name: [(randint(30, 60) * 100)  for _ in range(self.__length)]
            }
        )
        self.__data = data

        # return pd.DataFrame(data=data)



    def __generate_date_data(self):
        '''
        종료 일자가 시작 일자보다 커야 하므로 한 메소드에서 생성하지 않으면 귀찮아짐
        형식은 yyyy-MM-dd 문자열
        모집 기간 period는 폐구간 [14, 45] 내의 랜덤 값(단위: 일)
        offset은 폐구간 [1, period] 범위 내의 랜덤 값(단위: 일)
        시작 날짜는 offset일 전
        종료 날짜는 period-offset일 후
        따라서 모집 기간은 현재 날짜를 포함하는 period일이 됨
        '''
        period = randint(14, 45) # 모집 기간
        now = datetime.now().date() # 오늘 날짜
        
        start_dates = []
        end_dates = []
        for _ in range(self.__length):
            offset = randint(1, period)

            start_date = str(now - timedelta(days=offset))
            start_dates.append(start_date)

            end_date = str(now + timedelta(days=period - offset))
            end_dates.append(end_date)
        start_date_col = 'start_date'
        end_date_col = 'end_date'
        data = pd.DataFrame(
            data={
                start_date_col: start_dates,
                end_date_col: end_dates
            }
        )
        self.__data = data

        # return pd.DataFrame(data)


    def save(self) -> bool:
        excel_engine = 'xlsxwriter'
        csv_encoding = 'utf-8-sig'
        force_ascii = False
        index_col = 'seq'
        index = pd.DataFrame(
            data={
                index_col: list(range(1, self.__length + 1))
            }
        )
        data = pd.concat([self.__data, index], axis=1, ignore_index=False)        
        self.__data = data.set_index(index_col)
        try:
            if self.__format == self.EXCEL:
                self.__data.to_excel(excel_writer=self.__path, engine=excel_engine)
                return True
            elif self.__format == self.CSV:
                self.__data.to_csv(path_or_buf=self.__path, encoding=csv_encoding)
                return True
            elif self.__format == self.JSON:
                self.__data.to_json(path_or_buf=self.__path, force_ascii=force_ascii, orient='records', indent=4)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False