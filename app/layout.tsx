import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "The Log Exorcist - AI-Powered Log Analysis",
  description: "Transform messy error logs into actionable insights with AI-powered analysis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

