# cuma-webcrawler

커뮤니티 마스터 웹 크롤러

## 웹 크롤러 설정

1. source 폴더 추가
2. source 폴더에 json 파일 추가

   json 파일 예시

   ```json
   {
     "id": "dc_lol",
     "index": "site_dc",
     "site": "dc",
     "category": "lol",
     "category_name": "리그오브레전드 갤러리",
     "contents": "#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody",
     "site_type": "link",
     "host": "https://gall.dcinside.com",
     "link": {
       "type": "parameter/page",
       "url": "https://gall.dcinside.com/board/lists/?id=leagueoflegends6",
       "parameter": "page",
       "max_parameter": "5",
       "min_parameter": "1"
     },
     "info": {
       "subject": {
         "selector": "#container > section > article:nth-child(3) > div.view_content_wrap > header > div > h3 > span.title_subject",
         "meta": "name:title",
         "custom": ""
       },
       "content": {
         "selector": "#container > section > article:nth-child(3) > div.view_content_wrap > div > div.inner.clear > div.writing_view_box",
         "meta": "name:description",
         "custom": ""
       },
       "date": {
         "selector": "#container > section > article:nth-child(3) > div.view_content_wrap > header > div > div > div.fl > span.gall_date",
         "meta": "",
         "custom": ""
       },
       "view": {
         "selector": "#container > section > article:nth-child(3) > div.view_content_wrap > header > div > div > div.fr > span.gall_count",
         "meta": "",
         "custom": ""
       },
       "like": {
         "selector": "#container > section > article:nth-child(3) > div.view_content_wrap > div > div.positionr > div.btn_recommend_box.recomuse_y.morebox > div.inner_box > div:nth-child(1) > div > p:nth-child(1)",
         "meta": "",
         "custom": ""
       }
     }
   }
   ```

3. 패키지 설치

   ```bash
   poetry install
   ```

4. 가상화 설정

   ```bash
   poetry shell
   ```

5. 웹 크롤러 실행

   ```bash
   python run.py [id] [mode] [option]
   ```

## 수집 명령어

```bash
python run.py [id] [mode] [option]
```

- id : source 폴더에 있는 json 파일의 id
- mode
  - cra : 수집
- option
  - -json : json 파일로 저장
  - -debug : 디버그 모드
  - -test : 테스트 모드 (게시물 1개만 수집)
