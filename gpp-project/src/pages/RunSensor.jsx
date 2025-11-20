import React, { useState, useEffect } from "react";

function ErrorPopup({ message, onClose, title = "Message" }) {
  if (!message) return null;

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 backdrop-blur-sm">
      <div className="bg-[#0f0f0f] border border-gray-700 rounded-2xl p-6 max-w-md w-[90%] text-gray-200 shadow-2xl shadow-black/70">
        
        <h2 className="text-2xl font-bold mb-4 text-red-400 text-center">
          {title}
        </h2>

        <p className="mb-6 text-center leading-relaxed whitespace-pre-wrap">
          {message}
        </p>

        <div className="flex justify-center">
          <button
            onClick={onClose}
            className="px-6 py-2 border border-gray-600 rounded-lg text-gray-200 transition outline-none ring-0 
                       focus:ring-0 focus:outline-none hover:bg-[#1a1a1a] hover:border-gray-400 hover:text-white"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
}

function RunSensor() {

  useEffect(() => {
    document.title = "Radarix | Run Sensor";
  }, []);

  const [popupMessage, setPopupMessage] = useState("");
  const [popupTitle, setPopupTitle] = useState("");

  const handleRunSensor = () => {
    fetch("http://localhost:5001/run-sensor")
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setPopupTitle("Success!");
          setPopupMessage("Sensor started successfully!");
        } else {
          setPopupTitle("Sensor Error!");
          setPopupMessage("Sensor is not connected to the device. Kindly set it up and try again.");
        }
      })
      .catch(() => {
        setPopupTitle("Connection Error!");
        setPopupMessage("Cannot connect to backend. Run the backend server and try again.");
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
        className="mt-10 px-6 py-3 border border-gray-600 text-gray-200 rounded-lg transition outline-none ring-0 
                   focus:ring-0 focus:outline-none hover:bg-[#1a1a1a] hover:border-gray-400 hover:text-white"
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
