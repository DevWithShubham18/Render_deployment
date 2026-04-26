import Image from "next/image";
export default function ChatHeader() {
  return (
    <div className="sticky top-0 z-10 bg-white/80 backdrop-blur border-b border-gray-100">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-center gap-2">
        

        <Image
          src="/logo.png" 
          height={20}
          width={20}
          alt="Chartify Logo"
          className="h-8 w-8 object-contain"
        />

        <h1 className="text-base font-semibold tracking-tight text-gray-900">
          Chartify
        </h1>
      </div>
    </div>
  );
}