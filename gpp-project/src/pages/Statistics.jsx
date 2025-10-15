function Statistics() {
  return (
    <div className="w-screen min-h-screen flex flex-col justify-center items-center text-center bg-gray-50 px-6 md:px-20 py-32">
      <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
        Statistics
      </h1>
      <p className="text-lg md:text-xl text-gray-700 max-w-3xl leading-relaxed">
        View historical physiological data and analysis here.
        The system provides detailed insights and trends of heart rate, respiration,
        and movement patterns over time, helping in health monitoring and decision-making.
      </p>
    </div>
  );
}

export default Statistics;
