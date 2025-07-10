'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function UpdateProductPage() {
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
      setMessage('Missing state or location zone.')
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
      const res = await fetch('http://127.0.0.1:8000/update_product', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      const data = await res.json()

      if (!res.ok) throw new Error(data.detail || 'Update failed')
      setMessage('✅ Product updated!')
      setTimeout(() => router.push('/products/view'), 1500)
    } catch (err) {
      setMessage('❌ ' + err.message)
    }
  }

  return (
    <div className="max-w-md mx-auto p-6 mt-8 border border-black rounded shadow bg-white">
      <h2 className="text-xl font-bold text-black mb-4">Update Product</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {[
          { name: 'product_name', placeholder: 'Product Name' },
          { name: 'category', placeholder: 'Category' },
          { name: 'mrp', placeholder: 'MRP', type: 'number' },
          { name: 'manufacturing_date', type: 'date' },
          { name: 'expiry_date', type: 'date' },
          { name: 'inventory_level', placeholder: 'Inventory Level', type: 'number' },
        ].map(({ name, placeholder, type = 'text' }) => (
          <input
            key={name}
            name={name}
            type={type}
            placeholder={placeholder || name.replace('_', ' ')}
            value={form[name]}
            onChange={handleChange}
            required
            className="w-full border border-black text-black px-3 py-2 rounded"
          />
        ))}
        <button
          type="submit"
          className="w-full py-2 border border-black text-black rounded hover:bg-black hover:text-white transition"
        >
          ♻️ Update Product
        </button>
      </form>
      {message && <p className="mt-4 text-black text-center">{message}</p>}
    </div>
  )
}
