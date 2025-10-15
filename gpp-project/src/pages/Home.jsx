function Home() {
  return (
    <div className="flex flex-col items-center justify-start w-screen min-h-screen bg-black px-6 md:px-12 lg:px-20 pt-32 text-gray-200">
      <h1 className="text-5xl md:text-6xl font-extrabold mb-4">Radarix</h1>
      <h2 className="text-2xl md:text-3xl font-semibold mb-6 text-center">
        UWB Radar Based System for Physiological Signals
      </h2>
      <p className="text-lg md:text-xl max-w-3xl text-center">
        Radarix provides accurate, real-time, and non-contact monitoring of vital physiological signals using advanced UWB radar and AI technology.
      </p>
    </div>
  );
}

export default Home;
