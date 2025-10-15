import { useState, useEffect } from "react";

function Section({ title, children }) {
  const [open, setOpen] = useState(false);

  return (
    <div
      style={{
        borderBottom: "1px solid #ccc",
        width: "100%",
        padding: "20px 0",
      }}
    >
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

function App() {
  // Set body background and remove margin
  useEffect(() => {
    document.body.style.margin = 0;
    document.body.style.padding = 0;
    document.body.style.backgroundColor = "#f8f9fa";
  }, []);

  return (
    <div
      style={{
        fontFamily: "Arial, sans-serif",
        color: "#333",
        padding: "40px 60px",
        minHeight: "100vh",
        boxSizing: "border-box",
      }}
    >
      <header style={{ textAlign: "center", marginBottom: "40px" }}>
        <h1 style={{ fontSize: "36px" }}>UWB Radar-Based Physiological Signal Monitoring System</h1>
        <p
          style={{
            fontSize: "18px",
            maxWidth: "1200px",
            margin: "20px auto",
            lineHeight: "1.8",
            textAlign: "justify",
          }}
        >
          The UWB Radar-Based Physiological Signal Monitoring System is designed to provide continuous,
          accurate, and non-contact monitoring of vital signs such as heart rate, respiration, and movement.
          Combining radar sensing with AI-based signal processing, it delivers real-time health insights
          via an intuitive web interface for healthcare, fitness, and everyday environments.
        </p>
      </header>

      <main style={{ width: "100%", maxWidth: "1600px", margin: "0 auto" }}>
        <Section title="Overview">
          <p>
            Physiological signal monitoring is critical for health tracking. Traditional contact-based methods
            (ECG, pulse sensors) are uncomfortable and limit mobility. This system leverages UWB radar and AI
            to provide non-contact, precise, and real-time monitoring of heart rate, respiration, and movement
            patterns.
          </p>
        </Section>

        <Section title="System Workflow">
          <ol>
            <li>
              <strong>Signal Acquisition:</strong> UWB radar captures physiological signals non-intrusively.
            </li>
            <li>
              <strong>Signal Processing:</strong> Filters noise and extracts vital parameters with advanced algorithms.
            </li>
            <li>
              <strong>Health Monitoring:</strong> Detects abnormalities in heartbeat and breathing.
            </li>
            <li>
              <strong>User Interface:</strong> Displays real-time readings and alerts on a dashboard.
            </li>
            <li>
              <strong>System Robustness:</strong> Works reliably across different environments and users.
            </li>
          </ol>
        </Section>

        <Section title="Current Methods and Challenges">
          <ul>
            <li>Contact sensors are restrictive and uncomfortable.</li>
            <li>Wearables are prone to motion artifacts and require user compliance.</li>
            <li>Continuous monitoring is hard due to noise and environmental interference.</li>
          </ul>
        </Section>

        <Section title="Advantages of UWB Radar System">
          <ul>
            <li>Non-contact and hygienic monitoring.</li>
            <li>Detects micro-movements from heartbeat and breathing.</li>
            <li>Continuous monitoring in homes, hospitals, and fitness centers.</li>
            <li>AI-powered analysis ensures accuracy and early anomaly detection.</li>
          </ul>
        </Section>

        <Section title="Technical Design">
          <ol>
            <li><strong>Input:</strong> Raw UWB radar signals.</li>
            <li><strong>Preprocessing:</strong> Noise filtering, clutter removal, normalization.</li>
            <li><strong>Feature Extraction:</strong> Doppler and time-frequency analysis for vital signs.</li>
            <li><strong>Model Development:</strong> CNN, RNN, Transformer AI models.</li>
            <li><strong>Anomaly Detection:</strong> Flags abnormal heart or breathing patterns.</li>
            <li><strong>Output:</strong> Visualized metrics and alerts on the dashboard.</li>
          </ol>
        </Section>

        <Section title="Validation and Deployment">
          <p>
            System performance is measured using accuracy, sensitivity, specificity, and F1-score. Edge devices
            handle real-time monitoring while cloud systems manage analytics, storage, and model updates.
          </p>
        </Section>

        <Section title="Expected Outcomes">
          <ul>
            <li>Accurate non-contact measurement of heart rate and respiration.</li>
            <li>Detection of physiological anomalies.</li>
            <li>Real-time, user-friendly dashboard for health insights.</li>
            <li>Scalable for multiple environments.</li>
          </ul>
        </Section>

        <Section title="Benefits">
          <ul>
            <li>Comfortable and hygienic.</li>
            <li>Supports early health interventions.</li>
            <li>Applicable in healthcare, elderly care, and fitness.</li>
          </ul>
        </Section>

        <Section title="Challenges">
          <ul>
            <li>Environmental signal interference.</li>
            <li>Variability with posture, clothing, and distance.</li>
            <li>Hardware integration and cost considerations.</li>
          </ul>
        </Section>

        <Section title="Future Scope">
          <ul>
            <li>Multi-sensor fusion for improved accuracy.</li>
            <li>Extension to stress and mental health analysis.</li>
            <li>Integration with telemedicine and IoT healthcare platforms.</li>
          </ul>
          <p>
            UWB radar with AI enables accurate, continuous, and non-contact physiological monitoring,
            bridging comfort and precision for next-generation health solutions.
          </p>
        </Section>
      </main>
    </div>
  );
}

export default App;
