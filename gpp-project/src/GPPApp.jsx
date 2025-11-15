import { Routes, Route, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import About from "./pages/About";
import RunSensor from "./pages/RunSensor";
import Statistics from "./pages/Statistics";
import Login from "./pages/Login";

function GPPApp() {
  const location = useLocation();
  const hideLayout = location.pathname === "/login";

  return (
    <div className="font-sans bg-gray-50 min-h-screen">
      {!hideLayout && <Navbar />}

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/about" element={<About />} />
        <Route path="/run-sensor" element={<RunSensor />} />
        <Route path="/statistics" element={<Statistics />} />
        <Route path="/home" element={<Home  />} />
      </Routes>
    </div>
  );
}

export default GPPApp;
