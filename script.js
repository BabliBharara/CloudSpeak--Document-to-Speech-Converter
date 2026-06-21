async function convertFile() {
const fileInput = document.getElementById("fileInput");
const message = document.getElementById("message");

if (fileInput.files.length === 0) {
    message.innerHTML = "Please select a file.";
    return;
}

const file = fileInput.files[0];

message.innerHTML = "Uploading...";

const reader = new FileReader();

reader.onload = async function(event) {

    const base64String =
        event.target.result.split(",")[1];

    const payload = {
        fileName: file.name,
        fileContent: base64String
    };

    try {

        const response = await fetch(
            "https://jh9hh1y0e2.execute-api.ap-southeast-2.amazonaws.com/prod/upload",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const result = await response.json();

        const mp3Url =
`https://cloudspeak-output-babli.s3.ap-southeast-2.amazonaws.com/${result.audioFile}`;

        message.innerHTML = `
            ✅ Upload Successful!<br><br>

            <audio controls>
                <source src="${mp3Url}" type="audio/mpeg">
            </audio>

            <br><br>

            <a href="${mp3Url}" download>
                <button>Download MP3</button>
            </a>
        `;


    } catch (error) {

        message.innerHTML =
            "❌ Upload Failed";
    }
};

reader.readAsDataURL(file);
}
