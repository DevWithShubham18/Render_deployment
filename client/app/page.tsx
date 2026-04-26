import { auth } from "@/auth";
import ChatLayout from "./components/ChatLayout";
import SignIn from "./components/SignIn";
export default async function Page() {
  const session = await auth();

  
  if (!session) {
    return <SignIn />;
  }

  return <ChatLayout />;
}