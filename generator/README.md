# Data dictionary
|Column|Value|Type|
|:---:|:---|:---:|
|회사명|삼성SDS|CharField|
|회사 로고 URL|"https://cdn.worldvectorlogo.com/logos/trustpilot-1.svg"|CharField|
|포스터 이미지 URL|"https://s3.ap-northeast-2.amazonaws.com/terraform.eks.s3.bucket.for.lee.team/images/19.png"|CharField|
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

# Data generator
위 data dictionary에 맞게 데이터를 생성한다.
개인 프로젝트용으로 채용 공고 API를 제공하는 곳이 없어 데이터 생성기 사용이 불가피했다.
