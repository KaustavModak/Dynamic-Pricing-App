"use client";
import { usePathname } from "next/navigation";
import Navbar from "./Navbar";
import LoginNavbar from "./LoginNavbar"; // (Optional: if you want a custom one)

export default function NavbarWrapper() {
  const pathname = usePathname();

  
  if (pathname === "/login") return <LoginNavbar />;

  

  return <Navbar />;
}
