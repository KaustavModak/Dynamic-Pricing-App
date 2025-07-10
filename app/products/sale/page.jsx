'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function SalePage() {
  const [form, setForm] = useState({
    product_name: '',
    category: '',
    mrp: '',
    discount_applied: '',
    units_sold: '',
    date: '',  // ✅ Changed from `selling_date` to match backend
  })

  const [message, setMessage] = useState('')
  const router = useRouter()

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const state = localStorage.getItem('state')
    const location_zone = localStorage.getItem('tier')

    if (!state || !location_zone) {
      setMessage('❌ Missing state or location_zone in localStorage')
      return
    }

    const payload = {
      ...form,
      date: form.date,  // ✅ must be named `date`
      mrp: parseFloat(form.mrp),
      discount_applied: parseFloat(form.discount_applied),
      units_sold: parseInt(form.units_sold),
      state,
      location_zone,
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/new_sale', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || 'Sale failed')
      }

      setMessage('✅ Sale recorded successfully!')
      setTimeout(() => {
        setMessage('')
        router.push('/products/view')
      }, 1500)
    } catch (err) {
      console.error('Sale error:', err)
      setMessage('❌ ' + (err?.message || 'Unknown error'))
    }
  }

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 border border-black rounded">
      <h1 className="text-2xl font-bold mb-4 text-black">📊 Record a New Sale</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {[ 
          { name: 'product_name', type: 'text', placeholder: 'Product Name' },
          { name: 'category', type: 'text', placeholder: 'Category' },
          { name: 'mrp', type: 'number', placeholder: 'MRP (e.g. 100)' },
          { name: 'discount_applied', type: 'number', placeholder: 'Discount %' },
          { name: 'units_sold', type: 'number', placeholder: 'Units Sold' },
          { name: 'date', type: 'date', placeholder: 'Selling Date' },  // ✅ key updated
        ].map(({ name, type, placeholder }) => (
          <input
            key={name}
            name={name}
            type={type}
            placeholder={placeholder}
            value={form[name]}
            onChange={handleChange}
            required
            className="w-full border border-black text-black px-3 py-2 rounded"
          />
        ))}

        <button
          type="submit"
          className="w-full border border-black text-black font-semibold py-2 rounded hover:bg-black hover:text-white transition"
        >
          Submit Sale
        </button>
      </form>

      {message && (
        <p className="text-center mt-4 text-black">{message}</p>
      )}
    </div>
  )
}
