# cuma-webcrawler

커뮤니티 마스터 웹 크롤러

## 웹 크롤러 설정

1. source 폴더에 json 파일 추가

   json 파일 예시

   ```json
   {
     "id": "dc_lol",
     "index": "dc_lol",
     "site": "dc",
     "site_name": "디씨인사이드",
     "category": "lol",
     "category_name": "리그오브레전드 갤러리",
     "contents": "#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody",
     "link": {
       "type": "parameter/page",
       "url": "https://gall.dcinside.com/board/lists/?id=leagueoflegends6",
       "parameter": "page",
       "max_parameter": "5",
       "min_parameter": "1"
     },
     "info": {
       "subject": {
         "selector": "",
         "meta": "",
         "custom": ""
       },
       "content": {
         "selector": "",
         "meta": "",
         "custom": ""
       },
       "date": {
         "selector": "",
         "meta": "",
         "custom": ""
       },
       "view": {
         "selector": "",
         "meta": "",
         "custom": ""
       }
     }
   }
   ```

2. 패키지 설치

   ```bash
   poetry install
   ```

3. 가상화 환경 설정

   ```bash
   poetry shell
   ```

4. 웹 크롤러 실행

   ```bash
   python run.py [id]
   ```
