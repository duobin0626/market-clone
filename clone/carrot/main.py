from fastapi import FastAPI,UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('carrot.db',check_same_thread=False)
cur = con.cursor()

app = FastAPI()

#프론트엔드에서 받을 값 , 각 각 타입 지정필요.
@app.post('/items')
async def create_item(image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):
    
    # image_bytes : 이미지의 크기가 크기때문에 읽기위한 시간이 필요하여 처리 (async await)
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO 
                items(title,image, price, description, place,insertAt)
                VALUES
                ('{title}','{image_bytes.hex()}',{price},'{description}','{place}',{insertAt})
                """)    
    print(image, title, price, description, place) # 데이터값 확인용도
    con.commit() # 데이터가 들어감.
    return'200' # 200 = ok


# '/items' 호출시 응답할 API
@app.get('/items')
async def get_items():
    
    # 컬럼명도 같이 가져옴. 
    con.row_factory =sqlite3.Row
    
    # cur : DB를 가져오면서 con의 현재위치
    cur = con.cursor()
    
    # 컬럼명없이 가져오게 된다면 프론트엔드에서 각 값들을 판단해야 하기 때문에 
    # 데이터 처리에 편한 object 형식으로 보내주는게 좋다.
    rows = cur.execute(f"""
                       SELECT * FROM items;
                       """).fetchall()
    
    # [1,'test','test',....] → 컬럼명 없는 형식
    # rows = [[id:1],[title:'test'],[description:'test']...] → 컬럼명이 있는 형식
            
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))
    # dict(row) for row in rows → rows 중에 각각 array를 돌면서 
    # 그 array를 dictionary(객체 형태로 만들어 주는 문법) 형태로 만듬
    # { id:1, title:'test', description:'test'...}
    
    
# 이미지 응답하는 API 생성
@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    # image_bytes의 값은 16진수로 되어있을 꺼라서 .hex()를 사용하여 변환해줘야한다.
    image_bytes = cur.execute(f"""
                              SELECT image FROM items WHERE id={item_id}
                              """).fetchone()[0]
    
    return Response(content=bytes.fromhex(image_bytes))


# root path는 맨 밑에 작성해 주는것이 제일 좋다.
# root path는 모든 경로를 다 처리한다.
# api가 실행될 때 위에서 부터 차례차례 실행이 되는데 root가 위에 있으면 생성하는 api가 실행이 되지않기 때문
app.mount("/", StaticFiles(directory="static", html=True), name="static")