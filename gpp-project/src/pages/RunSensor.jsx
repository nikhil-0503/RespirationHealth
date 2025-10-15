function RunSensor() {
  return (
    <div className="flex flex-col items-center justify-start w-screen min-h-screen bg-black px-6 md:px-12 lg:px-20 pt-32 text-gray-200">
      <h1 className="text-5xl md:text-6xl font-extrabold mb-4">Run Sensor</h1>
      <h2 className="text-2xl md:text-3xl font-semibold mb-6 text-center">
        Start and View Real-Time Sensor Data
      </h2>
      <p className="text-lg md:text-xl max-w-3xl text-center">
        Use this page to initiate the UWB radar sensor and monitor live physiological signals instantly.
      </p>
    </div>
  );
}

export default RunSensor;
