import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import About from "./pages/About";
import RunSensor from "./pages/RunSensor";
import Statistics from "./pages/Statistics";

function GPPApp() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/run-sensor" element={<RunSensor />} />
        <Route path="/statistics" element={<Statistics />} />
      </Routes>
    </div>
  );
}

export default GPPApp;
