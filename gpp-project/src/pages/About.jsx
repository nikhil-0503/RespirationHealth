import Section from "../components/Section";

function About() {
  return (
    <div className="w-screen min-h-screen px-6 md:px-20 py-16 bg-gray-50">
      <h1 className="text-4xl md:text-5xl text-center font-bold mb-12 text-gray-900">
        About the System
      </h1>

      <main className="max-w-6xl mx-auto space-y-12">
        <Section title="Overview">
          <p className="text-lg md:text-xl text-gray-700 leading-relaxed">
            Physiological signal monitoring is critical for health tracking. Traditional contact-based methods
            (ECG, pulse sensors) are uncomfortable and limit mobility. This system leverages UWB radar and AI
            to provide non-contact, precise, and real-time monitoring of heart rate, respiration, and movement
            patterns.
          </p>
        </Section>

        <Section title="System Workflow">
          <ol className="list-decimal pl-6 space-y-3 text-gray-700 text-lg md:text-xl leading-relaxed">
            <li><strong>Signal Acquisition:</strong> UWB radar captures physiological signals non-intrusively.</li>
            <li><strong>Signal Processing:</strong> Filters noise and extracts vital parameters with advanced algorithms.</li>
            <li><strong>Health Monitoring:</strong> Detects abnormalities in heartbeat and breathing.</li>
            <li><strong>User Interface:</strong> Displays real-time readings and alerts on a dashboard.</li>
            <li><strong>System Robustness:</strong> Works reliably across different environments and users.</li>
          </ol>
        </Section>

        <Section title="Future Scope">
          <ul className="list-disc pl-6 space-y-2 text-gray-700 text-lg md:text-xl leading-relaxed">
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
