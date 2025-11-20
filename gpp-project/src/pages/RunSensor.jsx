import React, { useState } from "react";

function ErrorPopup({ message, onClose, title = "Message" }) {
  if (!message) return null;

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
      <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 max-w-md text-gray-200 shadow-xl">
        <h2 className="text-2xl font-bold mb-3 text-red-400">{title}</h2>

        <p className="mb-6 whitespace-pre-wrap">{message}</p>

        <button
          onClick={onClose}
          className="px-6 py-2 border border-gray-600 rounded-lg hover:bg-gray-800 transition"
        >
          Close
        </button>
      </div>
    </div>
  );
}

function RunSensor() {
  const [popupMessage, setPopupMessage] = useState("");
  const [popupTitle, setPopupTitle] = useState("");

const handleRunSensor = () => {
  fetch("http://localhost:5001/run-sensor")
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        setPopupTitle("Success");
        setPopupMessage("Sensor started successfully!");
      } else {
        // Ignore ugly Python error → show clean message instead
        setPopupTitle("Sensor Error");
        setPopupMessage("Sensor is not connected to the device.");
      }
    })
    .catch(() => {
      setPopupTitle("Connection Error");
      setPopupMessage("Cannot connect to backend.");
    });
};


  return (
    <div className="flex flex-col items-center justify-start w-screen min-h-screen bg-black px-6 md:px-12 lg:px-20 pt-20 text-gray-200">
      <h1 className="text-5xl md:text-6xl font-extrabold mb-4">Run Sensor</h1>

      <h2 className="text-2xl md:text-3xl font-semibold mb-6 text-center">
        Start and View Real-Time Sensor Data
      </h2>

      <p className="text-lg md:text-xl max-w-20xl text-center">
        Use this page to initiate the UWB radar sensor and monitor live physiological signals instantly.
      </p>

      {/* Run Sensor Button */}
      <button
        onClick={handleRunSensor}
        className="mt-10 px-6 py-3 border border-gray-600 text-gray-200 rounded-lg hover:bg-gray-800 transition"
      >
        Run the Sensor
      </button>

      {/* Popup Message */}
      <ErrorPopup
        message={popupMessage}
        title={popupTitle}
        onClose={() => setPopupMessage("")}
      />

      {/* Video Section */}
      <h3 className="text-3xl font-bold mt-16 mb-6 text-center">
        Steps to Setup the Sensor
      </h3>

      <div className="w-full max-w-3xl aspect-video rounded-xl overflow-hidden shadow-xl border border-gray-700">
        <iframe
          className="w-full h-full"
          src="https://www.youtube.com/embed/5CVs4GR3-nc"
          title="Sensor Setup Tutorial"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        ></iframe>
      </div>

      <br />
    </div>
  );
}

export default RunSensor;
