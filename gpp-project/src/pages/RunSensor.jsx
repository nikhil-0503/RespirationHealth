function RunSensor() {
  return (
    <div className="w-screen min-h-screen flex flex-col justify-center items-center text-center bg-gray-50 px-6 md:px-20 py-32">
      <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
        Run the Sensor
      </h1>
      <p className="text-lg md:text-xl text-gray-700 max-w-3xl leading-relaxed">
        Here you will be able to start and view real-time sensor data.
        The system provides live readings of heart rate, respiration, and movement
        patterns captured through UWB radar technology.
      </p>
    </div>
  );
}

export default RunSensor;
