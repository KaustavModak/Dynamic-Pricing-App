'use client';

import { useEffect, useState } from 'react';

export default function AccountPage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedId = localStorage.getItem('userId');

    if (!storedId) {
      setLoading(false);
      return;
    }

    fetch('/users.json')
      .then((res) => res.json())
      .then((data) => {
        const matched = data.find((u) => u.user_id === storedId);
        setUser(matched);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to fetch user data:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <p style={styles.message}>Loading user info...</p>;
  if (!user) return <p style={styles.message}>No user found. Please log in.</p>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        {/* <img src="/walmart-logo.png" alt="Walmart" style={styles.logo} /> */}
        <h1 style={styles.title}>Your Account</h1>
      </div>

      <div style={styles.card}>
        <h2 style={styles.cardTitle}>Account Details</h2>
        <div style={styles.detailRow}><strong>User ID:</strong> {user.user_id}</div>
        <div style={styles.detailRow}><strong>State:</strong> {user.state}</div>
        <div style={styles.detailRow}><strong>Tier:</strong> {user.location_zone}</div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    padding: '40px 20px',
    backgroundColor: '#F4F4F4',
    fontFamily: 'Segoe UI, sans-serif',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  header: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginBottom: '30px',
  },
  logo: {
    width: '120px',
    marginBottom: '10px',
  },
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#0071CE',
    textAlign: 'center',
  },
  card: {
    backgroundColor: '#FFFFFF',
    padding: '30px',
    borderRadius: '12px',
    boxShadow: '0 6px 16px rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '450px',
    borderLeft: '6px solid #FFC220',
  },
  cardTitle: {
    fontSize: '24px',
    color: '#0071CE',
    marginBottom: '20px',
    fontWeight: '600',
  },
  detailRow: {
    fontSize: '16px',
    color: '#333',
    marginBottom: '12px',
  },
  message: {
    textAlign: 'center',
    marginTop: '100px',
    fontSize: '18px',
    color: '#0071CE',
    fontWeight: '500',
  },
};
