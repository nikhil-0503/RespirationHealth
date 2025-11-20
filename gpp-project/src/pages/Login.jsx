import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (email === "admin@gpp.com" && password === "123456") {
      localStorage.setItem("logged_in", "true");  // IMPORTANT
      navigate("/home");
    } else {
      alert("Invalid login details");
    }
  };

  return (
    <div className="w-screen min-h-screen bg-black flex items-center justify-center text-gray-200 overflow-hidden">
      <div className="bg-gray-900 p-10 rounded-2xl shadow-xl w-[90%] max-w-md">

        <h2 className="text-3xl font-bold mb-6 text-center">Login</h2>

        <form onSubmit={handleSubmit} className="space-y-6">

          <div>
            <label className="block mb-1 text-sm font-medium">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 
                         focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block mb-1 text-sm font-medium">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 
                         focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 bg-blue-600 hover:bg-blue-700 
                       transition rounded-lg text-white font-semibold"
          >
            Login
          </button>
        </form>

      </div>
    </div>
  );
}
