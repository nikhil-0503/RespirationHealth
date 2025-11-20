import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    document.title = "Radarix";
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (email === "admin@gpp.com" && password === "123456") {
      localStorage.setItem("logged_in", "true");
      navigate("/home");
    } else {
      alert("Invalid login details");
    }
  };

  return (
    <div className="w-screen min-h-screen bg-black text-gray-200 overflow-hidden">

      {/* Add spacing below navbar */}
      <div className="pt-24 flex justify-center">

        <div className="bg-[#0f0f0f] p-10 rounded-2xl shadow-xl shadow-black/60 w-[90%] max-w-md border border-gray-800">
          
          <h2 className="text-3xl font-bold mb-6 text-center">Login</h2>

          <form onSubmit={handleSubmit} className="space-y-6">

            {/* Email */}
            <div>
              <label className="block mb-1 text-sm font-medium">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="
                  w-full px-4 py-2 rounded-lg
                  bg-[#111111] border border-gray-700 text-gray-200
                  focus:outline-none focus:ring-0 focus:border-gray-500
                "
              />
            </div>

            {/* Password */}
            <div>
              <label className="block mb-1 text-sm font-medium">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="
                  w-full px-4 py-2 rounded-lg
                  bg-[#111111] border border-gray-700 text-gray-200
                  focus:outline-none focus:ring-0 focus:border-gray-500
                "
              />
            </div>

            {/* Login Button */}
            <button
              type="submit"
              className="
                w-full py-2 rounded-lg font-semibold 
                bg-[#2a2a2a] border border-gray-700 text-gray-200
                hover:bg-[#333333] hover:border-gray-500 hover:text-white
                transition
              "
            >
              Login
            </button>

          </form>

        </div>

      </div>
    </div>
  );
}
