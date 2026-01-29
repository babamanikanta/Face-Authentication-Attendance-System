const video = document.getElementById("video");

// Start browser camera
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => (video.srcObject = stream))
  .catch(() => alert("Camera permission denied"));

// Capture image from video
function captureImage() {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  return canvas.toDataURL("image/jpeg");
}

// REGISTER
function register() {
  document.getElementById("status").innerText = "Registering... Look at the camera";

  const image = captureImage();

  fetch("http://127.0.0.1:5000/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      emp_id: document.getElementById("empId").value,
      name: document.getElementById("name").value,
      password: document.getElementById("password").value,
      image: image,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("status").innerText = data.message;
    })
    .catch(() => {
      document.getElementById("status").innerText = "Backend not running";
    });
}

// CHECK-IN / CHECK-OUT
function send(action) {
  document.getElementById("status").innerText = action.toUpperCase() + " ... Look at the camera";

  const image = captureImage();

  fetch(`http://127.0.0.1:5000/${action}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("status").innerText = data.message;
    });
}
