"use client";

import { signIn, useSession } from "next-auth/react";
import { useState } from "react";

export default function SignIn() {
  const { status } = useSession();
  const [loadingProvider, setLoadingProvider] = useState<string | null>(null);

  if (status === "loading") {
    return (
      <div className="flex min-h-[60vh] items-center justify-center text-sm text-gray-500">
        Loading session...
      </div>
    );
  }

  const handleLogin = async (provider: string) => {
    setLoadingProvider(provider);
    await signIn(provider, { callbackUrl: "/" });
  };

  return (
    <div className="flex min-h-[80vh] items-center justify-center px-4">
      <div className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
        
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-2xl font-semibold text-gray-900">
            Welcome to Chartify
          </h1>
          <p className="text-sm text-gray-500">
            Sign in to start generating charts
          </p>
        </div>

        {/* Buttons */}
        <div className="mt-6 space-y-3">
          
          <button
            onClick={() => handleLogin("github")}
            disabled={loadingProvider === "github"}
            className="w-full flex items-center justify-center gap-2 rounded-lg bg-black text-white py-2.5 text-sm font-medium hover:bg-gray-800 transition disabled:opacity-70 cursor-pointer"
          >
            {loadingProvider === "github" ? "Signing in..." : "Continue with GitHub"}
          </button>

        </div>

        {/* Footer */}
        <p className="mt-6 text-center text-xs text-gray-400">
          By continuing, you agree to our terms and privacy policy.
        </p>
      </div>
    </div>
  );
}