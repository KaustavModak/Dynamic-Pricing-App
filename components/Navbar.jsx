'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const pathname = usePathname();
  const isLogin = pathname === '/login';

  const navbarStyle = {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '7vh',
    backgroundColor: isLogin ? '#0070f3' : '#0070f3',
    color: isLogin ? '#0070f3' : '#000',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '40px',
    fontFamily: 'Arial',
    fontSize: '16px',
    zIndex: 1000,
  };

  const navlinkStyle = {
    color: isLogin ? '#0070f3' : '#000',
    textDecoration: 'none',
    fontWeight: 'bold',
  };

  return (
    <nav style={navbarStyle}>
      <Link href="/" style={navlinkStyle}>Home</Link>
      <Link href="/account" style={navlinkStyle}>Account</Link>
      <Link href="/contact" style={navlinkStyle}>Contact Us</Link>
      <Link href="/products" style={navlinkStyle}>Products</Link>
    </nav>
  );
}