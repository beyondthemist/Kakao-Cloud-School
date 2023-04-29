# Data generator
[Data dictionary](#data-dictionary)에 맞게 데이터를 생성한다.
개인 프로젝트용으로 채용 공고 API를 제공하는 곳이 없어 데이터 생성기 사용이 불가피했다.

<br>

# 사용법
```python
# main.py
generator = Generator(length=200, code=Generator.ALL, format=Generator.JSON)
generator.generate()
print('Saved.' if generator.save() else 'Not saved.')
```
- `length`: 생성할 record 수
- `code`: 생성할 컬럼. `Generator` 클래스의 상수로 지정한다. `ALL`로 설정하면 모든 컬럼의 데이터를 생성한다.
- `format`: 생성한 데이터를 저장할 형식. `.json`, `.xlsx`, `.csv`로 저장할 수 있다.

<br>

# Data dictionary
|Column|Value|Type|
|:---:|:---:|:---:|
|회사명|삼성SDS|CharField|
|회사 로고 URL|"https://cdn.worldvectorlogo.com/logos/trustpilot-1.svg"|CharField|
|포스터 이미지 URL|"https://s3.ap-northeast-2.amazonaws.com/s3.bucket.for.project/images/19.png"|CharField|
|공고 제목|삼성SDS IT 부문 채용|CharField|
|내용|삼성SDS에서 IT 직무 수행 인재 채용 중|CharField|
|직무|IT|CharField|
|지역|전북|CharField|
|기업 규모|중견기업|CharField|
|정규직|True|Boolean|
|경력직|False|Boolean|
|연봉(만원)|4200|IntegerField|
|채용 시작 날짜|2023-04-10|DateField|
|채용 종료 날짜|2023-04-24|DateField|

- 회사 이름과 회사 로고 URL은 크롤링으로 가져온다.
- 포스터는 크롤링이 어려워 50개 가량을 S3 버킷에 저장한 후 랜덤으로 꺼내어 썼다.
