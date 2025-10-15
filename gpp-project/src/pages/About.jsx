import Section from "../components/Section";

function About() {
  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "40px 60px", backgroundColor: "#f8f9fa" }}>
      <h1 style={{ textAlign: "center", fontSize: "32px" }}>About the System</h1>

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
            <li><strong>Signal Acquisition:</strong> UWB radar captures physiological signals non-intrusively.</li>
            <li><strong>Signal Processing:</strong> Filters noise and extracts vital parameters with advanced algorithms.</li>
            <li><strong>Health Monitoring:</strong> Detects abnormalities in heartbeat and breathing.</li>
            <li><strong>User Interface:</strong> Displays real-time readings and alerts on a dashboard.</li>
            <li><strong>System Robustness:</strong> Works reliably across different environments and users.</li>
          </ol>
        </Section>

        <Section title="Future Scope">
          <ul>
            <li>Multi-sensor fusion for improved accuracy.</li>
            <li>Extension to stress and mental health analysis.</li>
            <li>Integration with telemedicine and IoT healthcare platforms.</li>
          </ul>
        </Section>
      </main>
    </div>
  );
}

export default About;
