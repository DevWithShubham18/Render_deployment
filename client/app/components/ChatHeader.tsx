"use client";

import Image from "next/image";
import { useSession, signOut } from "next-auth/react";
import { useState } from "react";

export default function ChatHeader() {
  const { data: session } = useSession();
  const [open, setOpen] = useState(false);

  return (
    <div className="sticky top-0 z-10 bg-white/80 backdrop-blur border-b border-gray-100">
      <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        
        {/* Left: Logo */}
        <div className="flex items-center gap-2">
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

        {/* Right: User */}
        {session?.user ? (
          <div className="relative">
            <button
              onClick={() => setOpen(!open)}
              className="flex items-center gap-2 rounded-full px-2 py-1 hover:bg-gray-100 transition cursor-pointer"
            >
              {session.user.image ? (
                <Image
                  src={session.user.image}
                  alt="user"
                  width={28}
                  height={28}
                  className="rounded-full"
                />
              ) : (
                <div className="h-7 w-7 rounded-full bg-gray-300" />
              )}
            </button>

            {/* Dropdown */}
            {open && (
              <div className="absolute right-0 mt-2 w-56 rounded-xl border border-gray-200 bg-white shadow-lg p-2">
                
                <div className="px-3 py-2 border-b border-gray-100">
                  <p className="text-sm font-medium text-gray-900">
                    {session.user.name}
                  </p>
                  <p className="text-xs text-gray-500 truncate">
                    {session.user.email}
                  </p>
                </div>

                <button
                  onClick={() => signOut()}
                  className="w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg mt-1 cursor-pointer"
                >
                  Sign out
                </button>
              </div>
            )}
          </div>
        ) : (
          <button
            onClick={() => window.location.href = "/api/auth/signin"}
            className="text-sm font-medium px-3 py-1.5 rounded-lg border hover:bg-gray-50"
          >
            Sign in
          </button>
        )}
      </div>
    </div>
  );
}