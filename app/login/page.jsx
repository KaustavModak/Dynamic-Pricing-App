'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [id, setId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch('/users.json'); // assumes it's in /public
      const users = await res.json();

      const matchedUser = users.find(
        (user) => user.user_id === id && user.password === password
      );

      if (matchedUser) {
        // ✅ Store full user details for /account page
        localStorage.setItem('userId', matchedUser.user_id);
        localStorage.setItem('state', matchedUser.state);
        localStorage.setItem('tier', matchedUser.location_zone);
         const storedId = localStorage.getItem('userId');
        alert('Login successful!');
        router.push('/account');
      } else {
        setError('Invalid ID or Password');
      }
    } catch (err) {
      console.error('Error reading users.json:', err);
      setError('Login error');
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Login</h1>
      <form onSubmit={handleLogin} style={styles.form}>
        <input
          type="text"
          placeholder="Enter ID"
          value={id}
          onChange={(e) => setId(e.target.value)}
          style={styles.input}
          required
        />
        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
          required
        />
        {error && <p style={styles.error}>{error}</p>}
        <button type="submit" style={styles.button}>Login</button>
      </form>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '400px',
    margin: '100px auto',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '12px',
    textAlign: 'center',
    fontFamily: 'Arial',
  },
  title: {
    fontSize: '28px',
    marginBottom: '20px',
    color:'#000000'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
    color:'#000000',
  },
  input: {
    padding: '10px',
    fontSize: '16px',
  },
  button: {
    padding: '10px',
    fontSize: '16px',
    backgroundColor: '#0070f3',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
  },
  error: {
    color: 'red',
    fontSize: '14px',
  },
};
