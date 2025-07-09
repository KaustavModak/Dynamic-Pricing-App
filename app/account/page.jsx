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
      <h1 style={styles.title}>Account Details</h1>
      <div style={styles.card}>
        <p><strong>User ID:</strong> {user.user_id}</p>
        <p><strong>State:</strong> {user.state}</p>
        <p><strong>Tier:</strong> {user.location_zone}</p>
      </div>
    </div>
  );
}

const styles = {
  container: {
  minHeight: '100vh', // ✅ full screen height
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: '#ffffff',
  color: '#0ea5e9',
  fontFamily: 'Arial',
  textAlign: 'center',
  padding: '20px',
},

  title: {
    fontSize: '28px',
    marginBottom: '20px',
    color: '#0ea5e9', // sky blue title
  },
  card: {
    backgroundColor: '#ffffff', // white card background
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 0 10px rgba(14, 165, 233, 0.2)', // soft sky blue shadow
    textAlign: 'left',
    color: '#0ea5e9', // sky blue text in card
    border: '1px solid #0ea5e9',
  },
  message: {
    textAlign: 'center',
    marginTop: '100px',
    fontSize: '18px',
    color: '#0ea5e9',
  },
};
