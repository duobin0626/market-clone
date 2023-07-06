/* form 가져오기 */
const form = document.getElementById("write-form");

/*  form 데이터 서버로 전송 */
const handleSubmitForm = async (event) => {
  event.preventDefault();
  await fetch("/items", {
    method: "POST",
    body: new FormData(form),
  });
  console.log("okok");
};

form.addEventListener("submit", handleSubmitForm);
