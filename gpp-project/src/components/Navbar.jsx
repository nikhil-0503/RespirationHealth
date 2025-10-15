import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-around",
        alignItems: "center",
        padding: "15px 30px",
        backgroundColor: "#0d6efd",
        color: "white",
        fontWeight: "bold",
      }}
    >
      <Link to="/" style={{ color: "white", textDecoration: "none" }}>Home</Link>
      <Link to="/about" style={{ color: "white", textDecoration: "none" }}>About</Link>
      <Link to="/run-sensor" style={{ color: "white", textDecoration: "none" }}>Run Sensor</Link>
      <Link to="/statistics" style={{ color: "white", textDecoration: "none" }}>Statistics</Link>
    </nav>
  );
}

export default Navbar;
