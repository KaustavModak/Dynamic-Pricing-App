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
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable}`}
        style={{
          margin: 0,
          padding: 0,
          minHeight: "100vh",
          background: "linear-gradient(135deg, #0071CE, #005EA2)", // Walmart Blue Gradient
          color: "#333333",
        }}
      >
        {/* ✅ Retain your LoginNavbar */}
        <LoginNavbar />

        <main
          style={{
            marginTop: "7vh",
            padding: "40px 20px",
            minHeight: "calc(100vh - 7vh)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            boxSizing: "border-box",
          }}
        >
          <div
            style={{
              backgroundColor: "#ffffff",
              padding: "40px",
              borderRadius: "12px",
              boxShadow: "0 10px 30px rgba(0, 113, 206, 0.2)",
              width: "100%",
              maxWidth: "480px",
              borderLeft: "6px solid #FFC220", // Walmart Yellow accent
            }}
          >
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
