/* form 가져오기 */
const form = document.getElementById("write-form");

/*  form 데이터 서버로 전송 */
const handleSubmitForm = async (event) => {
  event.preventDefault();
  const body = new FormData(form);
  body.append("insertAt", new Date().getTime());
  try {
    const res = await fetch("/items", {
      method: "POST",
      body,
    });
    const data = await res.json();
    if (data === "200") window.location.pathname = "/";
  } catch (e) {
    console.error(e);
  }

  console.log("okok");
};

form.addEventListener("submit", handleSubmitForm);
