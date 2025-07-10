'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function DeleteProductPage() {
  const [product_name, setProductName] = useState('')
  const [message, setMessage] = useState('')
  const router = useRouter()

  const handleSubmit = async (e) => {
    e.preventDefault()

    const state = localStorage.getItem('state')
    const location_zone = localStorage.getItem('tier')

    if (!state || !location_zone) {
      setMessage('Missing state or location zone. Please login first.')
      return
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/delete_product', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_name, state, location_zone }),
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Failed to delete product.')
      }

      setMessage('✅ Product deleted successfully!')
      setTimeout(() => router.push('/products/view'), 1500)
    } catch (err) {
      console.error(err)
      setMessage(`❌ ${err.message}`)
    }
  }

  return (
    <div className="max-w-md mx-auto p-6 mt-8 bg-white shadow rounded border border-black">
      <h2 className="text-xl font-bold mb-4 text-black">Delete Product</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="product_name"
          placeholder="Product Name"
          value={product_name}
          onChange={(e) => setProductName(e.target.value)}
          required
          className="w-full border border-black text-black px-3 py-2 rounded"
        />

        <button
          type="submit"
          className="w-full border border-black text-black py-2 rounded hover:bg-black hover:text-white transition"
        >
          🗑️ Delete Product
        </button>
      </form>

      {message && (
        <p className="text-center mt-4 text-sm font-medium text-black">{message}</p>
      )}
    </div>
  )
}
