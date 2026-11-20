import { createFileRoute } from "@tanstack/react-router";
import mobile from "@/assets/mobile-clinic.jpg";
import { PageHero, Card, GhostButton, meta } from "@/components/site";

export const Route = createFileRoute("/outreach")({
  head: () => meta("Mobile clinics & charity", "MercyMed's mobile clinics bring free medical care to remote regions of Kyrgyzstan."),
  component: Outreach,
});

function Outreach() {
  return (
    <>
      <PageHero eyebrow="Mobile clinics" title="The charitable heart of our clinic" intro="We regularly travel to the regions to provide care where doctors are hard to reach." />
      <section className="container-site grid items-center gap-10 py-16 md:grid-cols-2">
        <img src={mobile} alt="Doctors examining patients outside a mobile clinic" loading="lazy" width={1408} height={912} className="rounded-3xl object-cover" />
        <div className="grid gap-4">
          <Card title="Where we go">Villages and towns across Kyrgyzstan's regions.</Card>
          <Card title="What we provide">Check-ups, basic medicines, screening and referrals.</Card>
          <Card title="How to help">Partner with us, volunteer or support a trip.</Card>
          <div><GhostButton to="/contact">Get involved</GhostButton></div>
        </div>
      </section>
    </>
  );
}
