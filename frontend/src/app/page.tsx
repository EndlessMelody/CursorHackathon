import ChatWindow from "@/components/ChatWindow";
import DocumentSidebar from "@/components/DocumentSidebar";

export default function Home() {
  return (
    <main className="flex h-screen w-full bg-slate-950">
      <DocumentSidebar />
      <div className="flex-1 h-full">
        <ChatWindow />
      </div>
    </main>
  );
}
