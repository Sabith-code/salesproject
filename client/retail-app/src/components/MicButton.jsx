import { Mic } from "lucide-react";
import { useVoiceRecorder } from "../hooks/useVoiceRecorder";

export default function MicButton() {
  const { startRecording, stopRecording, listening } = useVoiceRecorder();

  return (
    <button
      onMouseDown={startRecording}
      onMouseUp={stopRecording}
      className={`p-4 rounded-full shadow-lg transition ${
        listening ? "bg-red-500" : "bg-black"
      } text-white`}
    >
      <Mic />
    </button>
  );
}
