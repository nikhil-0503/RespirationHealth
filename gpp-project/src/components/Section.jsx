import { useState } from "react";

function Section({ title, children }) {
  const [open, setOpen] = useState(false);

  return (
    <div style={{ borderBottom: "1px solid #ccc", width: "100%", padding: "20px 0" }}>
      <button
        onClick={() => setOpen(!open)}
        style={{
          background: "none",
          border: "none",
          width: "100%",
          textAlign: "left",
          fontSize: "22px",
          fontWeight: "bold",
          cursor: "pointer",
          color: "#0d6efd",
          padding: "10px 20px",
        }}
      >
        {title} {open ? "▲" : "▼"}
      </button>
      <div
        style={{
          maxHeight: open ? "2000px" : "0px",
          overflow: "hidden",
          transition: "max-height 0.5s ease",
          paddingLeft: "30px",
          paddingRight: "30px",
        }}
      >
        {open && <div style={{ marginTop: "10px", lineHeight: "1.6", fontSize: "18px" }}>{children}</div>}
      </div>
    </div>
  );
}

export default Section;
