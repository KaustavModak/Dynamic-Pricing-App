export default function ContactPage() {
  const contacts = [
    {
      name: "HIYA DUTTA",
      email: "hiyadutta2255@gmail.com",
      linkedin: "https://www.linkedin.com/in/hiya-dutta/"
    },
    {
      name: "NABARUNA MUTSUDDI",
      email: "mutsuddinabaruna@gmail.com",
      linkedin: "https://www.linkedin.com/in/nabaruna-mutsuddi-8926b42a7/"
    },
    {
      name: "KAUSTAV MODAK",
      email: "kaustav.modak29@gmail.com",
      linkedin: "https://www.linkedin.com/in/kaustav-modak-214173276/"
    },
    {
      name: "PARAMBRATA ACHARJEE",
      email: "parambrataofficial@gmail.com",
      linkedin: "https://www.linkedin.com/in/parambrata-acharjee-662a85288/"
    }
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
      <h1 className="text-3xl font-bold text-blue-700 mb-8">Contact Us</h1>
      <div className="w-full max-w-2xl space-y-6">
        {contacts.map((contact, index) => (
          <div
            key={index}
            className="bg-white shadow-md rounded-lg p-5 border border-gray-200"
          >
            <h2 className="text-xl font-semibold text-gray-800">{contact.name}</h2>
            <p className="text-sm text-gray-600">
              Email: <a href={`mailto:${contact.email}`} className="text-blue-600 hover:underline">{contact.email}</a>
            </p>
            <p className="text-sm text-gray-600">
              LinkedIn:{" "}
              <a
                href={contact.linkedin}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline"
              >
                {contact.linkedin}
              </a>
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}