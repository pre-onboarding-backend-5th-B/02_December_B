# 소개

주식 투자를 위한 API 개발 프로젝트 입니다.

# 설계

## 요구사항

- <img src="https://user-images.githubusercontent.com/44486924/198935272-0187fd31-01c4-42f1-8a37-a6e2e26f7fb7.png" width="70%" height="70%" />
- 위의 이미지에 맞는 API를 만들것
- 데이터는 [asset_group_info_set.xlsx](https://github.com/pre-onboarding-backend-5th-B/02_December_B/files/9898195/asset_group_info_set.xlsx)
, [account_basic_info_set.xlsx](https://github.com/pre-onboarding-backend-5th-B/02_December_B/files/9898197/account_basic_info_set.xlsx)
, [account_asset_info_set.xlsx](https://github.com/pre-onboarding-backend-5th-B/02_December_B/files/9898198/account_asset_info_set.xlsx)
와 같이 주어지며 `batch`를 통해 매일 업데이트 할 수 있도록 한다.

## Batch

### 제약사항

- insert_company -> insert_asset -> insert_investment 순으로 실행되어야 한다.
- 파일 위치는 `/{django-project}/res/files/` 아래에 위치 한다.

### Commands 설명

- insert_company: asset_group_info_set.xlsx 을 읽어 들여 StockCompany Model 에 넣음
- insert_asset: account_asset_info_set.xlsx 을 읽어 들여 Account, StockBroker, StockCompany, Portfolio, PortfolioLog 에 insert
  한다.
- update_investment: account_basic_info_set.xlsx 파일을 읽어들여 Account Model에 계좌번호로 투자원금을 update 함

### 스케쥴링

```script
 0 0 * * * insert_company      # 매일 자정마다 insert_company 을 실행함
 10 0 * * * insert_asset       # 매일 00시 10분 마다 insert_asset 실행 함
 20 0 * * * update_investment  # 매일 00시 20분 마다 update_investment 을 실행 함 
```

### 명령어

```script
python manage.py insert_company
python manage.py insert_asset
python manage.py insert_investment
```

<details>
    <summary> <h2> 모델링 </h2></summary>

<details>
    <summary> <h3>고객(User)</h3> </summary>
- django user model 사용
</details>
<details>
<summary> <h3> 투자 계좌(Account) </summary>

- **id(pk)**
- 고객(user - fk)
- **계좌번호**(unique)
- 계좌명
- 계좌 총 자산
- 투자 원금
- 증권사

</details>
<details>
<summary> <h3> 증권사(StockBroker) </summary>

- **id(pk)**
- 증권사명

</details>
<details>
<summary> <h3> 그룹(Group) </summary>

- **id**
- 그룹명(미국 주식, 미국섹터 주식 등)

</details>
<details>
<summary> <h3> 투자하는 회사(StockCompany) </summary>

- **id(pk)**
- **그룹_id(fk)**
- **isin(unique)**
- 종목명
- 주식발행량
- 현재가

</details>
<details>
<summary> <h3> 고객의 보유 종목(Protfolio) </summary>

- **id(pk)**
- **계좌 id (fk)**
- **투자하는 회사_id (fk)**
- 보유 수량
- 매수가격(샀을 때 당시의 가격)
- 생성시간
- 수정시간

</details>
<details>
    <summary> <h3> 주문내역(Order) </summary>

- **계좌_id(fk)**
- **투자회사_id(fk)**
- 매수 가격
- 매수 주식 수
- ~~상태(status - true 입금까지 완료, false 완료되지 않은 거) → 만약 주문이 실패하면 삭제 or status updated_at~~
- 주문한 시간
- ~~updated_at~~

</details>

</details>

## API 목록

![image](https://user-images.githubusercontent.com/44486924/198943397-983908a5-99cc-4bad-9c28-d5a2ca6753db.png)
