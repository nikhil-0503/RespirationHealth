import { useEffect } from "react";

function About() {

  useEffect(() => {
    document.title = "Radarix | About";
  }, []);

  return (
    <div className="w-screen min-h-screen bg-black text-gray-200 px-6 md:px-12 lg:px-20 py-12">
      <h1 className="text-4xl md:text-5xl font-bold mb-12">About Radarix</h1>

      <main className="w-full flex-1 space-y-8">

        <section>
          <h2 className="text-2xl font-semibold mb-2">Overview</h2>
        </section>

      </main>
    </div>
  );
}

export default About;
