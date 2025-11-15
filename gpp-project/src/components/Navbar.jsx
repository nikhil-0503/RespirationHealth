import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-black/90 shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <div className="text-3xl md:text-3xl font-extrabold text-white">Radarix</div>
        <div className="space-x-6">
          <Link to="/home" className="text-gray-300 hover:text-white font-semibold">Home</Link>
          <Link to="/about" className="text-gray-300 hover:text-white font-semibold">About</Link>
          <Link to="/run-sensor" className="text-gray-300 hover:text-white font-semibold">Run Sensor</Link>
          <Link to="/statistics" className="text-gray-300 hover:text-white font-semibold">Statistics</Link>
          <Link to="/" className="text-gray-300 hover:text-white font-semibold">Login</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
