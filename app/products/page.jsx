'use client'

import { useRouter } from 'next/navigation'

export default function ProductsNav() {
  const router = useRouter()

  const buttons = [
    { label: 'View', path: '/products/view' },
    { label: 'Add New', path: '/products/add' },
    { label: 'Update', path: '/products/update' },
    { label: 'Delete', path: '/products/delete' },
    { label: 'Sale', path: '/products/sale' }, 
  ]

  return (
    <div className="flex gap-4 mb-6">
      {buttons.map((btn) => (
        <button
          key={btn.path}
          onClick={() => router.push(btn.path)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition"
        >
          {btn.label}
        </button>
      ))}
    </div>
  )
}