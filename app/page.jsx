'use client';
export default function Home() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-white">
      <h1 className="text-3xl sm:text-4xl font-bold text-blue-600 animate-fade-in">
        Welcome to Price Sparks
      </h1>

      <style jsx>{`
        .animate-fade-in {
          animation: fadeIn 1.2s ease-in-out;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}