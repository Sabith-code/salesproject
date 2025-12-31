import Sidebar from "./Sidebar";
import MicButton from "./MicButton";

export default function Layout({ children }) {
  return (
    <div className="flex h-screen">
      <Sidebar />

      <div className="flex-1 relative p-6">
        {children}

        <div className="absolute bottom-6 right-6">
          <MicButton />
        </div>
      </div>
    </div>
  );
}
