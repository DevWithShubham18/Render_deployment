export type Message = {
  role: "user" | "assistant";
  content?: string;
  config?: any; // chart
};
