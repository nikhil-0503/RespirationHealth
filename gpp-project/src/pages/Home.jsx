function Home() {
  return (
    <div className="flex flex-col justify-center items-center text-center w-screen min-h-screen bg-gradient-to-b from-gray-50 to-white px-4">
      <h1 className="text-6xl md:text-7xl font-extrabold text-gray-900 mb-4">Radarix</h1>
      <h2 className="text-2xl md:text-3xl font-medium text-gray-700 mb-6">
        UWB Radar Based System For Physiological Signals
      </h2>
      <p className="text-lg md:text-xl text-gray-600">
        Use the navigation bar to explore the system features.
      </p>
    </div>
  );
}

export default Home;
