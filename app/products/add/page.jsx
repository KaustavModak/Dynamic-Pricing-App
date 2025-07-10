'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function AddProductPage() {
  const [form, setForm] = useState({
    product_name: '',
    category: '',
    mrp: '',
    manufacturing_date: '',
    expiry_date: '',
    inventory_level: '',
  })
  const [message, setMessage] = useState('')
  const router = useRouter()

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const state = localStorage.getItem('state')
    const location_zone = localStorage.getItem('tier')

    if (!state || !location_zone) {
      setMessage('Missing state or location zone. Please login first.')
      return
    }

    const payload = {
      ...form,
      mrp: parseFloat(form.mrp),
      inventory_level: parseInt(form.inventory_level),
      state,
      location_zone,
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/new_product', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Something went wrong')
      }

      setMessage('✅ Product added successfully!')
      setTimeout(() => router.push('/products/view'), 1500)
    } catch (err) {
      console.error(err)
      setMessage(`❌ ${err.message}`)
    }
  }

  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow rounded mt-8">
      <h2 className="text-xl font-bold mb-4 text-blue-700">Add New Product</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="product_name"
          placeholder="Product Name"
          value={form.product_name}
          onChange={handleChange}
          required
          className="w-full border px-3 py-2 rounded"
        />
        <input
          name="category"
          placeholder="Category"
          value={form.category}
          onChange={handleChange}
          required
          className="w-full border px-3 py-2 rounded"
        />
        <input
          name="mrp"
          type="number"
          placeholder="MRP"
          value={form.mrp}
          onChange={handleChange}
          required
          className="w-full border px-3 py-2 rounded"
        />
        <input
          name="manufacturing_date"
          type="date"
          placeholder="Manufacturing Date"
          value={form.manufacturing_date}
          onChange={handleChange}
          required
          className="w-full border px-3 py-2 rounded"
        />
        <input
          name="expiry_date"
          type="date"
          placeholder="Expiry Date"
          value={form.expiry_date}
          onChange={handleChange}
          required
          className="w-full border px-3 py-2 rounded"
        />
        <input
          name="inventory_level"
          type="number"
          placeholder="Inventory Level"
          value={form.inventory_level}
          onChange={handleChange}
          required
          className="w-full border px-3 py-2 rounded"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          ➕ Add Product
        </button>
      </form>

      {message && (
        <p className="text-center mt-4 text-sm font-medium text-red-600">{message}</p>
      )}
    </div>
  )
}
