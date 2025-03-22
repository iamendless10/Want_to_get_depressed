import { useState } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [roast, setRoast] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("⚠️ Offer your PDF sacrifice first!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setRoast(data.roast);
    } catch (error) {
      console.error("Upload error:", error);
      alert("❌ The underworld rejected your resume!");
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-dark text-white font-elegant px-6">
      {/* 🔥 Title */}
      <h1 className="text-7xl md:text-8xl font-gothic text-ember mt-10 drop-shadow-xl animate-flicker text-center">
        ☠️ RESUME RITUAL ☠️
      </h1>

      {/* 🔥 Altar Box */}
      <div className="mt-12 p-12 bg-blood/40 border-4 border-ember rounded-3xl shadow-demon w-full max-w-2xl text-center">
        <label className="block text-3xl font-bold text-ember tracking-wider">
          🔥 Upload Your Soul 🔥
        </label>
        <input
          type="file"
          accept="application/pdf"
          className="mt-6 block w-full text-lg file:bg-blood file:text-white file:py-4 file:px-8 file:rounded-lg file:border-none file:cursor-pointer hover:file:bg-ember transition duration-300"
          onChange={handleFileChange}
        />
        <button
          className="mt-8 px-12 py-5 text-3xl bg-blood text-white font-bold rounded-2xl shadow-demon hover:bg-ember hover:shadow-lg transition-all duration-300 w-full"
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? "🔥 Summoning Roast..." : "☠️ OFFER YOUR RESUME ☠️"}
        </button>
      </div>

      {/* 🔥 Roast Result */}
      {roast && (
        <div className="mt-16 max-w-3xl bg-dark/90 p-12 border-4 border-ember rounded-3xl shadow-demon text-center">
          <h2 className="text-5xl font-gothic text-ember mb-6 animate-flicker">
            🔥 Your Fate is Sealed 🔥
          </h2>
          <p className="text-3xl text-red-300 leading-relaxed tracking-wide">
            {roast}
          </p>
        </div>
      )}
    </div>
  );
}
