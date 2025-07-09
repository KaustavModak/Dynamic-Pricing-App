// app/login/layout.js
import LoginNavbar from "../../components/LoginNavbar";
import { Geist, Geist_Mono } from "next/font/google";
import "../globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Login - Sparks Pricing",
};

export default function LoginLayout({ children }) {
  return (
    <html lang="en" style={{ backgroundColor: "#ffffff" }}>
      <body
        className={`${geistSans.variable} ${geistMono.variable}`}
        style={{
          margin: 0,
          padding: 0,
          backgroundColor: "#ffffff",
          minHeight: "100vh",
        }}
      >
        
        <main
          style={{
            marginTop: "7vh", // space below blue bar
            padding: "20px",
            backgroundColor: "#ffffff",
            minHeight: "calc(100vh - 7vh)",
            boxSizing: "border-box",
          }}
        >
          {children}
        </main>
      </body>
    </html>
  );
}
