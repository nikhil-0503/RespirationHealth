import React, { useState, useEffect } from "react";

function ErrorPopup({ message, onClose, title = "Message" }) {
  if (!message) return null;

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 backdrop-blur-sm">
      <div className="bg-[#0f0f0f] border border-gray-700 rounded-2xl p-6 max-w-md w-[90%] text-gray-200 shadow-2xl shadow-black/70">

        <h2 className="text-2xl font-bold mb-4 text-red-400 text-center">
          {title}
        </h2>

        <p 
          className="mb-6 leading-relaxed whitespace-pre-wrap text-gray-200"
          style={{
            maxHeight: "300px",
            overflowY: "auto",
            textAlign: "left",
            wordBreak: "break-word"
          }}
        >
          {message}
        </p>


        <div className="flex justify-center">
          <button
            onClick={onClose}
            className="px-6 py-2 border border-gray-600 rounded-lg text-gray-200 transition outline-none ring-0 
                       focus:ring-0 hover:bg-[#1a1a1a] hover:border-gray-400 hover:text-white"
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

  const [config, setConfig] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  // ML RESULTS
  const [predictedHR, setPredictedHR] = useState(null);
  const [hrClass, setHrClass] = useState(null);
  const [rrClass, setRrClass] = useState(null);
  const [stressClass, setStressClass] = useState(null);

  const userEmail = localStorage.getItem("loggedUser");

const handleRunSensor = () => {
  if (!userEmail) {
    setPopupTitle("Login Required");
    setPopupMessage("Please log in again. User email not found.");
    return;
  }

  if (config === null) {
    setPopupTitle("Configuration Missing");
    setPopupMessage("Please select Front or Back configuration before running the sensor.");
    return;
  }

  // 🔥 Show processing popup IMMEDIATELY
  setPopupTitle("Processing...");
  setPopupMessage("Starting sensor...\nCollecting data...\nCleaning...\nCalibrating...\nExtracting Features...\nAnalysing Data...");

  fetch("http://localhost:5002/run-sensor", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      userEmail: userEmail,
      configuration: config
    })
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {

        // ---- SHOW SUMMARY POPUP ----
        setPopupTitle("Vital Signs Summary");
        setPopupMessage(data.stats_text);

        // ---- SHOW ML RESULTS ON SCREEN ----
        if (data.ml_results) {
          const r = data.ml_results;

          setPredictedHR(r.Predicted_HR);
          setHrClass(r.HR_Class);
          setRrClass(r.RR_Class);
          setStressClass(r.Stress_Class);
        }

      } else {
        setPopupTitle("Sensor Error!");
        setPopupMessage(data.error || "Unknown error occurred while running sensor.");
      }
    })
    .catch(() => {
      setPopupTitle("Connection Error!");
      setPopupMessage("Cannot connect to backend. Run the backend server and try again.");
    });
};



  // COLOR FUNCTION ------------------------
const getColorClass = (label) => {
  if (!label) return "text-gray-300";

  const value = label.toLowerCase();

  if (["normal", "relaxed"].includes(value))
    return "text-green-400";

  if (["low", "moderate"].includes(value))
    return "text-yellow-400";

  if (["high", "stressed"].includes(value))
    return "text-red-400";

  return "text-gray-300";
};

  //----------------------------------------

  // ---------------------------------------------
  // PIPELINE: Upload → Cleaning → Calibration → ML
  // ---------------------------------------------
  const handleUploadCsv = async () => {
    if (!selectedFile) {
      setPopupTitle("No File Selected");
      setPopupMessage("Please upload a CSV file first.");
      return;
    }

    try {
      // Upload file
      setPopupTitle("Uploading...");
      setPopupMessage("Uploading CSV file...");
      
      const formData = new FormData();
      formData.append("file", selectedFile);

      const uploadRes = await fetch("http://localhost:5002/upload", {
        method: "POST",
        body: formData
      });

      const uploadData = await uploadRes.json();
      if (!uploadData.message) {
        setPopupTitle("Upload Error");
        setPopupMessage(uploadData.error || "Failed to upload CSV file.");
        return;
      }

      // Run pipeline
      setPopupTitle("Processing...");
      setPopupMessage("Cleaning...\nCalibrating...\nExtracting Features...\nAnalysing Data...");

      const pipeRes = await fetch("http://localhost:5002/run_pipeline", { method: "POST" });
      const pipeData = await pipeRes.json();

      if (pipeData.ml_results) {
        const r = pipeData.ml_results;

        // Store all ML results
        setPredictedHR(r.Predicted_HR);
        setHrClass(r.HR_Class);
        setRrClass(r.RR_Class);
        setStressClass(r.Stress_Class);

        setPopupTitle("Success!");
        setPopupMessage("Uploaded & Processed Successfully!\nFinal results displayed below.");

      } else {
        setPopupTitle("Pipeline Error");
        setPopupMessage(pipeData.error || "Pipeline failed.");
      }

    } catch (error) {
      setPopupTitle("Server Error");
      setPopupMessage("Backend not reachable. Please run Flask backend.");
    }
  };

  // UI START --------------------------------------------------
  return (
    <div className="flex flex-col items-center justify-start w-screen min-h-screen bg-black px-6 md:px-12 lg:px-20 pt-20 text-gray-200">

      <h1 className="text-5xl md:text-6xl font-extrabold mb-4">Run Sensor</h1>

      <h2 className="text-2xl md:text-3xl font-semibold mb-6 text-center">
        Start and View Real-Time Sensor Data
      </h2>

      <p className="text-lg md:text-xl max-w-20xl text-center mb-10">
        Use this page to initiate the UWB radar sensor and process physiological signals instantly.
      </p>

      {/* Configuration Section */}
      <div className="w-full max-w-xl bg-[#0f0f0f] border border-gray-700 rounded-xl p-6 mt-4 shadow-lg">
        <label className="block text-lg font-semibold mb-4 text-center">
          Choose the Person Configuration
        </label>

        <div className="flex flex-col gap-4">
          <label
            className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer border 
              ${config === 0 ? "border-gray-400 bg-[#1d1d1d]" : "border-gray-700 bg-[#131313] hover:border-gray-500"}`}
          >
            <input
              type="radio"
              name="configuration"
              value="0"
              checked={config === 0}
              onChange={() => setConfig(0)}
              className="w-4 h-4"
            />
            <span className="text-gray-200">Front Configuration</span>
          </label>

          <label
            className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer border 
              ${config === 1 ? "border-gray-400 bg-[#1d1d1d]" : "border-gray-700 bg-[#131313] hover:border-gray-500"}`}
          >
            <input
              type="radio"
              name="configuration"
              value="1"
              checked={config === 1}
              onChange={() => setConfig(1)}
              className="w-4 h-4"
            />
            <span className="text-gray-200">Back Configuration</span>
          </label>
        </div>
      </div>

      {/* Run Sensor Button */}
      <button
        onClick={handleRunSensor}
        className="mt-4 px-6 py-3 border border-gray-600 text-gray-200 rounded-lg transition hover:bg-[#1a1a1a] hover:border-gray-400 hover:text-white"
      >
        Run the Sensor
      </button>
      

{/* ---------------- CLEAN SENTENCE OUTPUT ---------------- */}
{predictedHR && (
  <div className="w-full max-w-3xl mt-10 text-center">

    {/* Heart Rate sentence */}
    <p className="text-2xl text-gray-200 mb-6">
      Your estimated heart rate is{" "}
      <span className="text-white font-bold">{predictedHR} bpm</span>.
    </p>

    {/* HR Class sentence */}
    <p className="text-xl text-gray-300 mb-3">
      Your heart rate category is{" "}
      <span className={`font-bold ${getColorClass(hrClass)}`}>
        {hrClass}
      </span>.
    </p>

    {/* RR Class sentence */}
    <p className="text-xl text-gray-300 mb-3">
      Your breathing rate is classified as{" "}
      <span className={`font-bold ${getColorClass(rrClass)}`}>
        {rrClass}
      </span>.
    </p>
  </div>
)}


      {/* Popup */}
      <ErrorPopup
        message={popupMessage}
        title={popupTitle}
        onClose={() => setPopupMessage("")}
      />

      {/* Video Tutorial */}
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
      <div className="w-full max-w-7xl mt-8 mb-12 text-center text-gray-400">
        <small>Radarix, 2025</small>
      </div>
    </div>
  );
}

export default RunSensor;
