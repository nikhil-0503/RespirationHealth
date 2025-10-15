import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <div className="text-xl font-bold text-gray-900">UWB Radar System</div>
        <div className="space-x-6">
          <Link to="/" className="text-gray-700 hover:text-gray-900 font-semibold">Home</Link>
          <Link to="/about" className="text-gray-700 hover:text-gray-900 font-semibold">About</Link>
          <Link to="/run-sensor" className="text-gray-700 hover:text-gray-900 font-semibold">Run Sensor</Link>
          <Link to="/statistics" className="text-gray-700 hover:text-gray-900 font-semibold">Statistics</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
