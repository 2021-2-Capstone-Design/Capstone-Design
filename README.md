# Capstone-Design Class06 Team5

1. 가상환경 만들기 & 장고 설치 : [점프투장고](https://wikidocs.net/book/4223) 참초
2. git clone https://github.com/2021-2-Capstone-Design/Capstone-Design
3. PAGE/mysite 의 내용을 1번에서 만든 projects/mysite 폴더에 이동시킨다.
4. [yolov3.weights](https://pjreddie.com/media/files/yolov3.weights) 다운후 mysite 폴더로 
5. cmd 창에서 mysite 임력 후 python manage.py runserver 실행
6. 주소창에 http://localhost:8000/anmu/ 입력
![image](https://user-images.githubusercontent.com/76734572/144621000-d3d93cd8-69ed-4306-89e1-e4f1a2459540.png)






---
## 사용 방법
<메인페이지>

1. 연습을 할 수 있는 Practice 페이지로 이동

  a) 이미 존재하는 안무로 연습할 때
     - Play Video 버튼을 누르면 웹캠과 VLC를 통해 연습을 진행함
   (여기서 웹캠 영상은 저장됨)
     - 점수 보기를 누르면 저장된 웹캠 영상에서 관절 좌표를 추출하고, 
       기존 영상과 벡터 연산을 진행하여 결과 출력 

  b) 없는 안무를 연습하고 싶을 때 (1인)
     - Upload Video 버튼을 눌러 안무 영상 추가하는 것을 진행 
     - 1인을 선택하면 해당 영상에서 관절 좌표 추출하여 저장 
     - a)와 동일하게 연습 진행 및 벡터 연산 결과 출력 

  c) 없는 안무를 연습하고 싶을 때 (2인)
     - Upload Video 버튼을 눌러 안무 영상 추가하는 것을 진행 
     - 2인을 선택하면 해당 영상의 Cropping 과정을 진행함 
     - 따라할 인물을 선택하면 관절 좌표 추출하여 저장 
     - a)와 동일하게 연습 진행 및 벡터 연산 결과 출력 

1-a) demo_intro -> demo_practice -> demo_film -> demo_score
1-b)                             -> demo_upload -> demo_film -> demo_score
1-c)                                            -> demo_extract -> demo_film -> demo_score


2. 기록을 확인할 수 있는 History 페이지로 이동

2  ) demo_intro -> demo_history
