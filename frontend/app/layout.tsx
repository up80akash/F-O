import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "F&O Trading Platform",
  description: "AI-powered Indian F&O trading platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
