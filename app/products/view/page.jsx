'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function ProductViewPage() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const router = useRouter()

  useEffect(() => {
    const state = localStorage.getItem('state')
    const location_zone = localStorage.getItem('tier')

    console.log("📦 Fetching products for:", { state, location_zone })

    // 🛑 Redirect to login if no state or tier
    if (!state || !location_zone) {
      setError('Missing state or location zone. Redirecting...')
      setTimeout(() => {
        router.push('/login')  // Change this if your login route is different
      }, 1500)
      setLoading(false)
      return
    }

    fetch('http://127.0.0.1:8000/products', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state, location_zone }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Server responded with ${res.status}`)
        }
        return res.json()
      })
      .then((data) => {
        if (data.products && Array.isArray(data.products)) {
          setProducts(data.products)
        } else {
          setError(data.message || 'No products found.')
        }
      })
      .catch((err) => {
        console.error('❌ Fetch error:', err)
        setError('Failed to fetch products from backend.')
      })
      .finally(() => {
        setLoading(false)
      })
  }, [router])

  if (loading) {
    return <p className="text-center mt-10 text-blue-600">🔄 Loading products...</p>
  }

  if (error) {
    return <p className="text-center mt-10 text-red-500">{error}</p>
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold text-blue-700 mb-4">🛍️ Available Products</h1>
      {products.length === 0 ? (
        <p className="text-center text-gray-600">No products available in your region.</p>
      ) : (
        <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {products.map((product, idx) => (
            <li key={idx} className="border rounded-lg p-4 shadow bg-white">
              <h2 className="text-lg font-semibold">{product.product_name}</h2>
              <p>Category: {product.category}</p>
              <p>MRP: ₹{product.mrp}</p>
              <p>Final Price: ₹{product.final_price}</p>
              <p>Expiry Days: {product.expiry_days}</p>
              <p>Inventory: {product.inventory_level}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
