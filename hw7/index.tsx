import { createFileRoute, Link } from "@tanstack/react-router";
import hero from "@/assets/hero-clinic.jpg";
import mobile from "@/assets/mobile-clinic.jpg";
import { BookButton, GhostButton, Card, CtaBand, CLINIC, meta } from "@/components/site";

export const Route = createFileRoute("/")({
  head: () => meta("Evidence-based medical care", "MercyMed is a Bishkek medical center offering evidence-based, international medicine for locals, expats and travellers. Book an appointment online."),
  component: Index,
});

const AUDIENCES = [
  { to: "/services", title: "I need a doctor", text: "Consultations, lab tests and check-ups for adults and children." },
  { to: "/corporate", title: "We're an organisation", text: "Yearly staff check-ups, student programs and embassy partnerships." },
  { to: "/education", title: "I'm in medical training", text: "Placements for residents and medical students." },
] as const;

function Index() {
  return (
    <>
      <section className="container-site grid items-center gap-12 py-14 md:grid-cols-2 md:py-20">
        <div>
          <p className="text-sm font-bold uppercase tracking-widest text-brand-red">Medical center · Bishkek</p>
          <h1 className="mt-4 text-4xl font-extrabold leading-tight md:text-6xl">
            Compassionate care for{" "}
            <span className="bg-brand-gradient bg-clip-text text-transparent">body and spirit.</span>
          </h1>
          <p className="mt-6 max-w-lg text-lg text-muted-foreground">
            Evidence-based, international medicine delivered by locally trained professionals — in English, Kyrgyz and Russian.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <BookButton />
            <GhostButton to="/services">Explore our services</GhostButton>
          </div>
        </div>
        <div className="relative">
          <div className="absolute -inset-3 -z-10 rotate-2 rounded-3xl bg-brand-gradient opacity-80" />
          <img src={hero} alt="A MercyMed doctor consulting a patient" width={1600} height={1008} className="aspect-[4/3] w-full rounded-3xl object-cover" />
        </div>
      </section>

      <section className="container-site pb-16">
        <div className="grid gap-4 md:grid-cols-3">
          {AUDIENCES.map((a) => (
            <Link key={a.to} to={a.to} className="group rounded-2xl border bg-card p-6 transition hover:shadow-soft">
              <h2 className="text-lg font-semibold">{a.title}</h2>
              <p className="mt-2 text-muted-foreground">{a.text}</p>
              <span className="mt-4 inline-block text-sm font-bold text-brand-red group-hover:underline">Learn more →</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="bg-secondary/60 py-16">
        <div className="container-site">
          <h2 className="text-3xl font-bold">Why MercyMed</h2>
          <div className="mt-8 grid gap-4 md:grid-cols-3">
            <Card title="Evidence-based">Treatment guided by international standards and current research — no unnecessary tests or medicines.</Card>
            <Card title="International & local">Care that works for locals, expats and travellers alike, in three languages.</Card>
            <Card title="A charitable heart">Our mobile clinics bring free care to remote regions of Kyrgyzstan.</Card>
          </div>
        </div>
      </section>

      <section className="container-site grid items-center gap-10 py-16 md:grid-cols-2">
        <img src={mobile} alt="MercyMed mobile clinic in a mountain village" loading="lazy" width={1408} height={912} className="rounded-3xl object-cover" />
        <div>
          <h2 className="text-3xl font-bold">Care beyond the city</h2>
          <p className="mt-4 text-muted-foreground">Every visit to MercyMed helps fund mobile clinics in the regions, where specialist care is hard to reach.</p>
          <div className="mt-6"><GhostButton to="/outreach">See our mobile clinics</GhostButton></div>
        </div>
      </section>

      <section className="container-site pb-4 text-center">
        <h2 className="text-2xl font-bold">Follow us on Instagram</h2>
        <p className="mt-2 text-muted-foreground">News, health tips and photos from the clinic.</p>
        <a href={CLINIC.instagram} target="_blank" rel="noreferrer" className="mt-5 inline-flex rounded-full bg-brand-gradient px-6 py-3 text-sm font-bold text-primary-foreground">
          @mercymed.kg
        </a>
      </section>

      <CtaBand />
    </>
  );
}
