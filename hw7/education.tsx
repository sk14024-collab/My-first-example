import { createFileRoute } from "@tanstack/react-router";
import { PageHero, Card, GhostButton, meta } from "@/components/site";

export const Route = createFileRoute("/education")({
  head: () => meta("Medical education", "Clinical training for residents and medical students in evidence-based family medicine at MercyMed."),
  component: Education,
});

function Education() {
  return (
    <>
      <PageHero eyebrow="Medical education" title="Training the next generation" intro="We partner with hospitals and medical schools to train residents and students in evidence-based medicine." />
      <section className="container-site grid gap-4 py-16 md:grid-cols-3">
        <Card title="Residents">Supervised clinical rotations in outpatient family medicine.</Card>
        <Card title="Medical students">Observation and hands-on learning alongside our doctors.</Card>
        <Card title="Institutions">Long-term collaborations with hospitals and medical schools.</Card>
      </section>
      <section className="container-site pb-16"><GhostButton to="/contact">Ask about placements</GhostButton></section>
    </>
  );
}
