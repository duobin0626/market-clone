from fastapi import FastAPI,UploadFile,Form
from fastapi.staticfiles import StaticFiles
from typing import Annotated

app = FastAPI()

#프론트엔드에서 받을 값 , 각 각 타입 지정필요.
@app.post('/items')
def create_item(image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()]):
    print(image, title, price, description, place)
    return'200' # 200 = ok


# root path는 맨 밑에 작성해 주는것이 제일 좋다.
# root path는 모든 경로를 다 처리한다.
# api가 실행될 때 위에서 부터 차례차례 실행이 되는데 root가 위에 있으면 생성하는 api가 실행이 되지않기 때문
app.mount("/", StaticFiles(directory="static", html=True), name="static")