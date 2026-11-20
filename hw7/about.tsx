import { createFileRoute } from "@tanstack/react-router";
import { PageHero, Card, CtaBand, meta } from "@/components/site";

export const Route = createFileRoute("/about")({
  head: () => meta("About us", "Our mission, vision, values and history — revolutionising healthcare in Kyrgyzstan through a holistic approach of body and spirit."),
  component: About,
});

function About() {
  return (
    <>
      <PageHero eyebrow="About MercyMed" title="Holistic healthcare for Kyrgyzstan" intro="We exist to improve the quality of life of our patients through competent, compassionate and comprehensive medical care." />
      <section className="container-site grid gap-10 py-16 md:grid-cols-2">
        <div>
          <h2 className="text-2xl font-bold">Our vision</h2>
          <p className="mt-3 text-muted-foreground">To revolutionise the way healthcare is delivered in Kyrgyzstan through a holistic approach of body and spirit.</p>
          <h2 className="mt-10 text-2xl font-bold">What we bring to Kyrgyzstan</h2>
          <p className="mt-3 text-muted-foreground">Evidence-based, internationally aligned medicine provided by locally trained professionals — and a commitment to train the next generation of doctors here at home.</p>
        </div>
        <div>
          <h2 className="text-2xl font-bold">Our history</h2>
          <ol className="mt-5 space-y-5 border-l-2 border-primary pl-6">
            <li><p className="font-semibold">Founded</p><p className="text-muted-foreground">MercyMed opens its doors in Bishkek. (Add year and story.)</p></li>
            <li><p className="font-semibold">First mobile clinic</p><p className="text-muted-foreground">Care reaches patients in the regions. (Add details.)</p></li>
            <li><p className="font-semibold">Today</p><p className="text-muted-foreground">A growing team serving patients, organisations and medical trainees.</p></li>
          </ol>
        </div>
      </section>
      <section className="bg-secondary/60 py-16">
        <div className="container-site">
          <h2 className="text-2xl font-bold">Our values</h2>
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            {["Compassion", "Holistic care", "Integrity", "Trust", "Sustainability"].map((v) => (
              <Card key={v} title={v}>{""}</Card>
            ))}
          </div>
        </div>
      </section>
      <CtaBand />
    </>
  );
}
