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
- `django-crontab` 을 이용하여 스케쥴링을 함
- cron 명령어
  - **cron 추가**
  ```shell
  (env)$project_dir>python manage.py crontab add  # cron 추가
  
  adding cronjob: ... -> ('0 0 * * *', 'django.core.management.call_command', ['insert_company'], {}, '>> /$PROJECT_DIR/log/insert_company 2>&1')
  adding cronjob: ... -> ('10 0 * * *', 'django.core.management.call_command', ['insert_asset'], {}, '>> /$PROJECT_DIR/log/insert_asset 2>&1')
  adding cronjob: ... -> ('20 0 * * *', 'django.core.management.call_command', ['update_investment'], {}, '>> /$PROJECT_DIR/log/update_investment 2>&1')
  ```
  - **cron 제거**
  ```shell
  (env)$project_dir>python manage.py crontab remove  # cron 삭제
  
  removing cronjob: ... -> ('0 0 * * *', 'django.core.management.call_command', ['insert_company'], {}, '>> /$PROJECT_DIR/log/insert_company 2>&1')
  removing cronjob: ... -> ('10 0 * * *', 'django.core.management.call_command', ['insert_asset'], {}, '>> /$PROJECT_DIR/log/insert_asset 2>&1')
  removing cronjob: ... -> ('20 0 * * *', 'django.core.management.call_command', ['update_investment'], {}, '>> /$PROJECT_DIR/log/update_investment 2>&1')
  ```
  - **cron 보기**
  ```shell
  (env)$project_dir>python manage.py crontab remove  # cron 삭제
  Currently active jobs in crontab:
  ... -> ('0 0 * * *', 'django.core.management.call_command', ['insert_company'], {}, '>> /$PROJECT_DIR/log/insert_company 2>&1')
  ... -> ('10 0 * * *', 'django.core.management.call_command', ['insert_asset'], {}, '>> /$PROJECT_DIR/log/insert_asset 2>&1')
  ... -> ('20 0 * * *', 'django.core.management.call_command', ['update_investment'], {}, '>> /$PROJECT_DIR/log/update_investment 2>&1')
  ```
  
- 스케쥴 시간대
```shell
 0 0 * * * insert_company      # 매일 자정마다 insert_company 을 실행함
 10 0 * * * insert_asset       # 매일 00시 10분 마다 insert_asset 실행 함
 20 0 * * * update_investment  # 매일 00시 20분 마다 update_investment 을 실행 함 
```

### batch 명령어

```shell
(env)$project_dir>python manage.py insert_company     # 우선 실행
(env)$project_dir>python manage.py insert_asset       # 그 다음 실행
(env)$project_dir>python manage.py update_investment  # 마지막 실행
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
    <summary> <h3> 송금내역(Transfer) </summary>

- **계좌_id(fk)**
- 송금액
- 상태
  - 송금상태를 뜻한다. `P`는 Pending `S`는 송금이 완료된 상태
- 송금 시간

</details>

</details>

## API 목록
### Transfer - 송금 기능
1. `GET` /transfer
   - 송금 목록을 조회 한다.
2. `POST` /transfer
   - **절차 1**을 실행한다
     - 절차 1은 송금을 보내기 전 유효한 요청인 지 판단한다.
     - 요청 데이터로는 `계좌 id`와 `금액` 이 있다.
   - request 
     ```json
     {
        "account": "1",
        "price": "1000"  // 100 보다는 큰 금액을 보내야 함 
     }
     ```
   - response
     - 201
       ```json
       {
          "signature": "30300f183f336e340bcfbd99c5545724ab3bc262aa70368a33f059c901d601e3",
          "transfer_id": 23
       }
       ```
     - 400 
       ```json
       {
         "price": [
             "Ensure this value is greater than or equal to 100."
          ]
       }
       ```
3. `GET` /transfer/:id
   - 송금과 관련된 시그니처와 송금 상태를 확인할 수 있다. 
     - `P` 는 절차 1를 통과했지만 송금이 완료되지는 않은 상태이다.
     - `S` 는 송금이 완료된 상태이다.
4. `PATCH` /transfer/:id 
  - 송금을 보내는 요청이다.
  - request
    ```json
    {
      "signature": "30300f183f336e340bcfbd99c5545724ab3bc262aa70368a33f059c901d601e3",
    }
    ```
  - response:
    - 200
      ```json
      {
        "status": "S" // 완료된 상태
      }
      ```
    - 400
      ```json
      {
        "message": "transfer id 를 확인하세요"
      }
      ```