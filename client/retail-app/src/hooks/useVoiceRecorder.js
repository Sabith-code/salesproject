import { useRef, useState } from "react";

export function useVoiceRecorder() {
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const streamRef = useRef(null);

  const [listening, setListening] = useState(false);

  const startRecording = async () => {
    // ⛔ Prevent double start
    if (listening) return;

    streamRef.current = await navigator.mediaDevices.getUserMedia({ audio: true });

    const recorder = new MediaRecorder(streamRef.current);
    mediaRecorderRef.current = recorder;
    chunksRef.current = [];

    recorder.ondataavailable = (e) => {
      chunksRef.current.push(e.data);
    };

    recorder.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: "audio/webm" });

      console.log("🎤 AUDIO BLOB:", blob);
      console.log("📦 SIZE (bytes):", blob.size);

      // cleanup
      streamRef.current.getTracks().forEach(track => track.stop());
      mediaRecorderRef.current = null;
      chunksRef.current = [];
    };

    recorder.start();
    setListening(true);
  };

  const stopRecording = () => {
    // ⛔ Prevent invalid stop
    if (!mediaRecorderRef.current || !listening) return;

    mediaRecorderRef.current.stop();
    setListening(false);
  };

  return {
    startRecording,
    stopRecording,
    listening,
  };
}
