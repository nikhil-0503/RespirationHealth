function About() {
  return (
    <div className="w-full min-h-screen bg-gray-50 px-6 md:px-12 lg:px-20 py-12 flex flex-col">
      <h1 className="text-4xl md:text-5xl text-center font-bold mb-12 text-gray-900">
        About the System
      </h1>

      <main className="w-full flex-1 space-y-8">

        <section>
          <h2 className="text-2xl font-semibold mb-2">Overview</h2>
          <p>
            Physiological signal monitoring is critical for health tracking. Traditional contact-based methods
            (ECG, pulse sensors) are uncomfortable and limit mobility. This system leverages UWB radar and AI
            to provide non-contact, precise, and real-time monitoring of heart rate, respiration, and movement
            patterns.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">System Workflow</h2>
          <ol className="list-decimal pl-6 space-y-2">
            <li><strong>Signal Acquisition:</strong> UWB radar captures physiological signals non-intrusively.</li>
            <li><strong>Signal Processing:</strong> Filters noise and extracts vital parameters with advanced algorithms.</li>
            <li><strong>Health Monitoring:</strong> Detects abnormalities in heartbeat and breathing.</li>
            <li><strong>User Interface:</strong> Displays real-time readings and alerts on a dashboard.</li>
            <li><strong>System Robustness:</strong> Works reliably across different environments and users.</li>
          </ol>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">Current Methods and Challenges</h2>
          <ul className="list-disc pl-6 space-y-1">
            <li>Contact sensors are restrictive and uncomfortable.</li>
            <li>Wearables are prone to motion artifacts and require user compliance.</li>
            <li>Continuous monitoring is hard due to noise and environmental interference.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">Advantages of UWB Radar System</h2>
          <ul className="list-disc pl-6 space-y-1">
            <li>Non-contact and hygienic monitoring.</li>
            <li>Detects micro-movements from heartbeat and breathing.</li>
            <li>Continuous monitoring in homes, hospitals, and fitness centers.</li>
            <li>AI-powered analysis ensures accuracy and early anomaly detection.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">Technical Design</h2>
          <ol className="list-decimal pl-6 space-y-2">
            <li><strong>Input:</strong> Raw UWB radar signals.</li>
            <li><strong>Preprocessing:</strong> Noise filtering, clutter removal, normalization.</li>
            <li><strong>Feature Extraction:</strong> Doppler and time-frequency analysis for vital signs.</li>
            <li><strong>Model Development:</strong> CNN, RNN, Transformer AI models.</li>
            <li><strong>Anomaly Detection:</strong> Flags abnormal heart or breathing patterns.</li>
            <li><strong>Output:</strong> Visualized metrics and alerts on the dashboard.</li>
          </ol>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">Validation and Deployment</h2>
          <p>
            System performance is measured using accuracy, sensitivity, specificity, and F1-score. Edge devices
            handle real-time monitoring while cloud systems manage analytics, storage, and model updates.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">Expected Outcomes</h2>
          <ul className="list-disc pl-6 space-y-1">
            <li>Accurate non-contact measurement of heart rate and respiration.</li>
            <li>Detection of physiological anomalies.</li>
            <li>Real-time, user-friendly dashboard for health insights.</li>
            <li>Scalable for multiple environments.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">Benefits</h2>
          <ul className="list-disc pl-6 space-y-1">
            <li>Comfortable and hygienic.</li>
            <li>Supports early health interventions.</li>
            <li>Applicable in healthcare, elderly care, and fitness.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">Challenges</h2>
          <ul className="list-disc pl-6 space-y-1">
            <li>Environmental signal interference.</li>
            <li>Variability with posture, clothing, and distance.</li>
            <li>Hardware integration and cost considerations.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-2">Future Scope</h2>
          <ul className="list-disc pl-6 space-y-1">
            <li>Multi-sensor fusion for improved accuracy.</li>
            <li>Extension to stress and mental health analysis.</li>
            <li>Integration with telemedicine and IoT healthcare platforms.</li>
          </ul>
          <p className="mt-2">
            UWB radar with AI enables accurate, continuous, and non-contact physiological monitoring,
            bridging comfort and precision for next-generation health solutions.
          </p>
        </section>

      </main>
    </div>
  );
}

export default About;
