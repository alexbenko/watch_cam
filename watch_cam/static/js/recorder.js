if (MediaRecorder.notSupported) {
  noSupport.style.display = 'block'
  dictaphone.style.display = 'none'
}

function handlerFunction(stream) {
  rec = new MediaRecorder(stream);
  rec.ondataavailable = e => {
    audioChunks.push(e.data);
    if (rec.state == "inactive"){
      const recordedAudio = document.getElementById("recorded-audio")
      let blob = new Blob(audioChunks,{type:'audio/mpeg-3'});
      recordedAudio.src = URL.createObjectURL(blob);
      recordedAudio.controls=true;
      recordedAudio.autoplay=true;
      sendData(blob)
    }
  }
}
function sendData(data) {
  console.log(data)
}

const record = document.getElementById("start-record")
const stopRecord = document.getElementById("stop-record")

navigator.mediaDevices.getUserMedia({audio:true}).then(stream => {handlerFunction(stream)})
record.onclick = (e) => {
  console.log('record was clicked')
  record.disabled = true;
  record.style.backgroundColor = "blue"
  stopRecord.disabled=false;
  audioChunks = [];
  rec.start();
}
stopRecord.onclick = (e) => {
  console.log("stopRecord was clicked")
  record.disabled = false;
  stop.disabled=true;
  record.style.backgroundColor = "red"
  rec.stream.getTracks().forEach(i => i.stop())
}