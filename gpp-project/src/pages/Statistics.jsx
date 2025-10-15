function Statistics() {
  return (
    <div className="flex flex-col items-center justify-start w-screen min-h-screen bg-black px-6 md:px-12 lg:px-20 pt-32 text-gray-200">
      <h1 className="text-5xl md:text-6xl font-extrabold mb-4">Statistics</h1>
      <h2 className="text-2xl md:text-3xl font-semibold mb-6 text-center">
        Historical Physiological Data
      </h2>
      <p className="text-lg md:text-xl max-w-3xl text-center">
        Analyze historical trends of heart rate, respiration, and movement patterns to gain insights for better health monitoring and decision-making.
      </p>
    </div>
  );
}

export default Statistics;
