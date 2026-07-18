import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Anime Calendar — Demo Dashboard",
  description: "A personalized anime release intelligence dashboard.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
