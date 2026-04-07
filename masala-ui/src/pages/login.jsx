import { useState } from "react";
import axios from "axios";
import bg from "../assets/bg.jpg";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/api/auth/login/", form);
      localStorage.setItem("token", res.data.access);
      alert("Login successful 🚀");
    } catch (err) {
      alert("Invalid credentials ❌");
    }
  };

  return (
   <div
  className="h-screen w-full flex items-center justify-center bg-cover bg-center bg-no-repeat"
  style={{ backgroundImage: `url(${bg})` }}
>
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/50"></div>

      {/* Glass Card */}
      <div className="relative z-10 backdrop-blur-lg bg-white/10 border border-white/20 p-8 rounded-2xl shadow-xl w-80 text-white animate-fadeIn">
        
        <h2 className="text-2xl font-bold text-center mb-6">
          Jhaagirdar Masale 🌶️
        </h2>

        <input
          type="text"
          placeholder="Username"
          className="w-full p-2 mb-4 rounded bg-white/20 outline-none"
          onChange={(e) => setForm({ ...form, username: e.target.value })}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 mb-4 rounded bg-white/20 outline-none"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <button
          onClick={handleLogin}
          className="w-full bg-yellow-500 hover:bg-yellow-600 transition p-2 rounded font-semibold"
        >
          Login
        </button>
      </div>
    </div>
  );
}