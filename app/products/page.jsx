'use client'

import { useState, useEffect } from 'react'

export default function ProductsPage() {
  const [products, setProducts] = useState([])
  const [form, setForm] = useState({
    id: '',
    product_name: '',
    category: '',
    mrp: '',
    final_price: '',
    inventory_level: '',
    expiry_days: '',
  })
  const [mode, setMode] = useState('list') // modes: list, insert, update, delete

  const fetchProducts = async () => {
    try {
      const res = await fetch('http://localhost:8000/products')
      const data = await res.json()
      setProducts(data)
    } catch (error) {
      console.error('Error fetching products:', error)
    }
  }

  useEffect(() => {
    fetchProducts()
  }, [])

  const handleInputChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const insertProduct = async () => {
    try {
      await fetch('http://localhost:8000/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, id: parseInt(form.id) }),
      })
      fetchProducts()
    } catch (error) {
      console.error('Error inserting product:', error)
    }
  }

  const updateProduct = async () => {
    try {
      await fetch(`http://localhost:8000/products/${form.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, id: parseInt(form.id) }),
      })
      fetchProducts()
    } catch (error) {
      console.error('Error updating product:', error)
    }
  }

  const deleteProduct = async () => {
    try {
      await fetch(`http://localhost:8000/products/${form.id}`, {
        method: 'DELETE',
      })
      fetchProducts()
    } catch (error) {
      console.error('Error deleting product:', error)
    }
  }

  return (
    <div className="p-6">
      {/* Mode selection buttons */}
      <div className="space-x-4 mb-4">
        <button onClick={() => setMode('list')} className="bg-gray-200 px-4 py-2 rounded">
          List
        </button>
        <button onClick={() => setMode('insert')} className="bg-green-500 text-white px-4 py-2 rounded">
          Insert
        </button>
        <button onClick={() => setMode('update')} className="bg-yellow-500 text-white px-4 py-2 rounded">
          Update
        </button>
        <button onClick={() => setMode('delete')} className="bg-red-500 text-white px-4 py-2 rounded">
          Delete
        </button>
      </div>

      {/* Form Section */}
      {(mode === 'insert' || mode === 'update' || mode === 'delete') && (
        <div className="space-y-4 mb-4">
          <input type="text" name="id" value={form.id} onChange={handleInputChange} placeholder="ID" className="border px-2 py-1 w-full" />
          {(mode === 'insert' || mode === 'update') && (
            <>
              <input name="product_name" value={form.product_name} onChange={handleInputChange} placeholder="Product Name" className="border px-2 py-1 w-full" />
              <input name="category" value={form.category} onChange={handleInputChange} placeholder="Category" className="border px-2 py-1 w-full" />
              <input name="mrp" value={form.mrp} onChange={handleInputChange} placeholder="MRP" className="border px-2 py-1 w-full" />
              <input name="final_price" value={form.final_price} onChange={handleInputChange} placeholder="Final Price" className="border px-2 py-1 w-full" />
              <input name="inventory_level" value={form.inventory_level} onChange={handleInputChange} placeholder="Inventory Level" className="border px-2 py-1 w-full" />
              <input name="expiry_days" value={form.expiry_days} onChange={handleInputChange} placeholder="Expiry Days" className="border px-2 py-1 w-full" />
            </>
          )}
          {mode === 'insert' && (
            <button onClick={insertProduct} className="bg-green-600 text-white px-4 py-2 rounded">
              Add Product
            </button>
          )}
          {mode === 'update' && (
            <button onClick={updateProduct} className="bg-yellow-600 text-white px-4 py-2 rounded">
              Update Product
            </button>
          )}
          {mode === 'delete' && (
            <button onClick={deleteProduct} className="bg-red-600 text-white px-4 py-2 rounded">
              Delete Product
            </button>
          )}
        </div>
      )}

      {/* Product List */}
      {mode === 'list' && (
        <ul className="space-y-4">
          {products.map((p) => (
            <li key={p.id} className="border p-4 rounded shadow">
              <strong>{p.product_name}</strong> - ₹{p.final_price} ({p.category})  
              <br />
              MRP: ₹{p.mrp} | Inventory: {p.inventory_level} | Expiry: {p.expiry_days} days
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
