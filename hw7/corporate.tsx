import { createFileRoute } from "@tanstack/react-router";
import { PageHero, Card, GhostButton, meta } from "@/components/site";

export const Route = createFileRoute("/corporate")({
  head: () => meta("For organisations", "Partner with MercyMed for yearly staff check-ups, student health programs and embassy medical services in Bishkek."),
  component: Corporate,
});

function Corporate() {
  return (
    <>
      <PageHero eyebrow="For organisations" title="A trusted medical partner for your people" intro="Embassies, schools and companies rely on MercyMed for regular, high-quality medical care." />
      <section className="container-site grid gap-4 py-16 md:grid-cols-3">
        <Card title="Yearly staff check-ups">Tailored annual examinations for your team, scheduled around your workday.</Card>
        <Card title="Schools & students">Special packages for students and school medical requirements.</Card>
        <Card title="Embassies & NGOs">International-standard care for staff and their families.</Card>
      </section>
      <section className="container-site pb-16">
        <div className="rounded-3xl bg-secondary p-10">
          <h2 className="text-2xl font-bold">Let's talk partnership</h2>
          <p className="mt-2 max-w-xl text-muted-foreground">Tell us about your organisation and we'll prepare an offer.</p>
          <div className="mt-6"><GhostButton to="/contact">Contact us</GhostButton></div>
        </div>
      </section>
    </>
  );
}
