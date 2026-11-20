import { createFileRoute } from "@tanstack/react-router";
import { PageHero, CtaBand, meta } from "@/components/site";

export const Route = createFileRoute("/services")({
  head: () => meta("Medical services", "Consultations, laboratory tests, check-ups, vaccinations and more at MercyMed in Bishkek."),
  component: Services,
});

// Edit services and prices here.
const SERVICES = [
  { name: "General consultation", desc: "Adults and children, with a family medicine doctor.", price: "from — som" },
  { name: "Laboratory tests", desc: "Blood, urine and other common tests with fast results.", price: "from — som" },
  { name: "Health check-ups", desc: "Yearly preventive check-up packages.", price: "from — som" },
  { name: "Vaccinations", desc: "Routine and travel vaccines.", price: "from — som" },
  { name: "Travel medicine", desc: "Advice and care for travellers and tourists.", price: "from — som" },
  { name: "Chronic disease care", desc: "Diabetes, blood pressure and long-term follow-up.", price: "from — som" },
];

function Services() {
  return (
    <>
      <PageHero eyebrow="Medical services" title="What we can help with" intro="Clear, evidence-based care. Not sure what you need? Book a consultation and we'll guide you." />
      <section className="container-site py-16">
        <div className="divide-y rounded-2xl border bg-card">
          {SERVICES.map((s) => (
            <div key={s.name} className="flex flex-col gap-1 p-6 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-lg font-semibold">{s.name}</h2>
                <p className="text-muted-foreground">{s.desc}</p>
              </div>
              <p className="font-semibold text-brand-red">{s.price}</p>
            </div>
          ))}
        </div>
      </section>
      <CtaBand />
    </>
  );
}
