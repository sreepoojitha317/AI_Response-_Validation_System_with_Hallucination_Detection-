// ==========================================================
// RESPONSE TYPE SWITCHING
// ==========================================================

const responseTypes = document.querySelectorAll(
    'input[name="type"]'
);

const textSection =
document.getElementById("text-section");

const pdfSection =
document.getElementById("pdf-section");

const voiceSection =
document.getElementById("voice-section");

responseTypes.forEach(type => {

    type.addEventListener(
        "change",
        function(){

            textSection.classList.add("hidden");
            pdfSection.classList.add("hidden");
            voiceSection.classList.add("hidden");

            if(this.value === "text"){

                textSection.classList.remove("hidden");

            }

            else if(this.value === "pdf"){

                pdfSection.classList.remove("hidden");

            }

            else if(this.value === "voice"){

                voiceSection.classList.remove("hidden");

            }

        }

    );

});


// ==========================================================
// PDF FILE NAME DISPLAY
// ==========================================================

const pdfInput =
document.getElementById("pdf-file");

pdfInput.addEventListener(
"change",
function(){

    if(this.files.length > 0){

        const fileName =
        this.files[0].name;

        document.querySelector(
            ".upload-area p"
        ).innerHTML =
        fileName;

    }

});


// ==========================================================
// VOICE RECORDING
// ==========================================================

const micButton =
document.getElementById("mic-button");

const voiceStatus =
document.getElementById("voice-status");

let mediaRecorder;
let audioChunks = [];
let recording = false;

let timer;
let seconds = 0;

micButton.addEventListener(
"click",
async function(){

    if(!recording){

        startRecording();

    }

    else{

        stopRecording();

    }

});

async function startRecording(){

    try{

        const stream =
        await navigator.mediaDevices.getUserMedia(
            {
                audio:true
            }
        );

        mediaRecorder =
        new MediaRecorder(stream);

        audioChunks = [];

        mediaRecorder.start();

        recording = true;

        micButton.style.animation =
        "pulse 1s infinite";

        voiceStatus.innerHTML =
        "🔴 Recording started...";

        startTimer();

        mediaRecorder.ondataavailable =
        event =>{

            audioChunks.push(
                event.data
            );

        };

        mediaRecorder.onstop =
        ()=>{

            const audioBlob =
            new Blob(
                audioChunks,
                {
                    type:"audio/webm"
                }
            );

            console.log(
                "Recorded Audio:",
                audioBlob
            );

            voiceStatus.innerHTML =
            "✅ Voice recorded successfully";

        };

    }

    catch(error){

        alert(
            "Microphone permission denied"
        );

        console.log(error);

    }

}

function stopRecording(){

    mediaRecorder.stop();

    mediaRecorder.stream
    .getTracks()
    .forEach(
        track=>track.stop()
    );

    recording=false;

    micButton.style.animation =
    "none";

    stopTimer();

}


// ==========================================================
// RECORDING TIMER
// ==========================================================

function startTimer(){

    seconds=0;

    timer=setInterval(
        ()=>{

            seconds++;

            let min =
            Math.floor(seconds/60);

            let sec =
            seconds%60;

            voiceStatus.innerHTML =

            `🔴 Recording ${min}:${sec < 10 ?
            "0"+sec : sec}`;

        },
        1000
    );

}

function stopTimer(){

    clearInterval(timer);

}


// ==========================================================
// EVALUATE BUTTON
// CALL FASTAPI API
// ==========================================================

const evaluateButton =
document.getElementById(
    "evaluate-button"
);

evaluateButton.addEventListener(
"click",
async function(){

    const question =
    document.getElementById(
        "question"
    ).value.trim();

    const aiResponse =
    document.getElementById(
        "text-response"
    ).value.trim();

    const reference =
    document.getElementById(
        "reference"
    ).value.trim();

    if(question===""){

        alert(
            "Please enter a question."
        );

        return;

    }

    if(aiResponse===""){

        alert(
            "Please enter the AI response."
        );

        return;

    }

    evaluateButton.disabled = true;

    evaluateButton.innerHTML =
    "Evaluating...";

    try{

        const response =
        await fetch(
            "/evaluate",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    question:question,

                    ai_response:aiResponse,

                    reference:reference

                })

            }
        );

        if(!response.ok){

            throw new Error(
                "Evaluation failed."
            );

        }

        const result =
        await response.json();

        console.log(result);

        sessionStorage.removeItem("batch_result");

        sessionStorage.setItem(
            "evaluation_result",
            JSON.stringify(result)
        );

        window.location.href="/results";

    }

    catch(error){

        console.error(error);

        alert(
            "Unable to evaluate response."
        );

    }

    finally{

        evaluateButton.disabled = false;

        evaluateButton.innerHTML =
        "Evaluate Response";

    }

});

/* ==========================================================
   Batch CSV FILE NAME DISPLAY
========================================================== */

const batchInput = document.getElementById("batch-file");

if (batchInput) {

    batchInput.addEventListener("change", function () {

        if (this.files.length > 0) {

            const fileName = this.files[0].name;

            const uploadArea = this.closest(".upload-area");

            uploadArea.querySelector("p").textContent = fileName;

            uploadArea.querySelector("span").textContent =
                "CSV selected successfully ✅";

        }

    });

}


/* ==========================================================
   Batch Evaluation
========================================================== */

const batchButton = document.getElementById("batch-btn");

if (batchButton) {

    batchButton.addEventListener("click", async function () {

        if (!batchInput.files.length) {

            alert("Please select a CSV file.");

            return;

        }

        const formData = new FormData();

        formData.append(
            "file",
            batchInput.files[0]
        );

        batchButton.disabled = true;

        batchButton.innerHTML = "Evaluating...";

        try {

            const response = await fetch(
                "/batch-evaluate",
                {
                    method: "POST",
                    body: formData
                }
            );

            if (!response.ok) {

                throw new Error("Batch evaluation failed.");

            }

            const result = await response.json();

            console.log(result);

            sessionStorage.removeItem("evaluation_result");

            sessionStorage.setItem(
                "batch_result",
               JSON.stringify(result)
            );


            window.location.href="/results?batch=true";
        }

        catch (error) {

            console.error(error);

            alert("Batch Evaluation Failed.");

        }

        finally {

            batchButton.disabled = false;

            batchButton.innerHTML = "Evaluate CSV";

        }

    });

}