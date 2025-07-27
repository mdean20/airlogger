import type { Metadata } from "next";
import "@/styles/globals.scss";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "AirLogger - Aircraft Flight Tracking",
  description: "Track flight hours and financial performance for N593EH",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
