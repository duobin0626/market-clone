/* const renderData = (data) => {
  //   data.forEach((obj) => console.log(obj.id));
  // 서버에서 가져온 데이터를 이용하여 html 생성
  const main = document.querySelector("main");
  data.forEach((obj) => {
    const div = document.createElement("div");
    div.innerText = obj.title;
    main.appendChild(div);
  });
}; */

const calcTime = (timeStamp) => {
  // 세계시간(curTime)으로 출력.
  // 한국시간 : UTC +9
  const curTime = new Date().getTime() - 9 * 60 * 60 * 1000; // 9시간 * 60분 * 60초 * 1000ms
  const time = new Date(curTime - timeStamp);
  const hour = time.getHours();
  const minutes = time.getMinutes();
  const second = time.getSeconds();

  if (hour > 0) return `${hour}시간 전`;
  else if (minutes > 0) return `${minutes}분 전`;
  else if (second > 0) return `${second}초 전`;
  else return "방금 전";
};

const renderData = (data) => {
  const main = document.querySelector("main");

  // .reverse() : 최신시간이 위로 오게끔 정렬 바꾸는것
  data.reverse().forEach(async (obj) => {
    const div = document.createElement("div");
    div.className = "item-list";

    const imgDiv = document.createElement("div");
    imgDiv.className = "item-list__img";

    const infoDiv = document.createElement("div");
    infoDiv.className = "item-list__info";

    const img = document.createElement("img");
    const res = await fetch(`/images/${obj.id}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    img.src = url;

    const infoTitleDiv = document.createElement("p");
    infoTitleDiv.className = "item-list__info-title";
    infoTitleDiv.innerText = obj.title;

    const infoMetaDiv = document.createElement("span");
    infoMetaDiv.className = "item-list__info-meta";
    infoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAt);

    const infoPriceDiv = document.createElement("strong");
    infoPriceDiv.className = "item-list__info-price";
    infoPriceDiv.innerText = obj.price;

    imgDiv.appendChild(img);
    infoDiv.appendChild(infoTitleDiv);
    infoDiv.appendChild(infoMetaDiv);
    infoDiv.appendChild(infoPriceDiv);
    div.appendChild(imgDiv);
    div.appendChild(infoDiv);
    main.appendChild(div);
  });
};

// 서버에서 데이터를 불러와서 받는 코드
const fetchList = async () => {
  const res = await fetch("/items");
  const data = await res.json();
  renderData(data);
};

fetchList();
