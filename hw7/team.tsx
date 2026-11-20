import { createFileRoute } from "@tanstack/react-router";
import { PageHero, CtaBand, meta } from "@/components/site";

export const Route = createFileRoute("/team")({
  head: () => meta("Our team", "Meet the doctors, nurses and staff of MercyMed medical center in Bishkek."),
  component: Team,
});

// Edit team members here — add a photo URL to show a picture.
const TEAM: { name: string; role: string; bio: string; photo?: string }[] = [
  { name: "Team member", role: "Family physician", bio: "Short bio — training, languages, interests." },
  { name: "Team member", role: "Pediatrician", bio: "Short bio — training, languages, interests." },
  { name: "Team member", role: "Nurse", bio: "Short bio — training, languages, interests." },
  { name: "Team member", role: "Lab technician", bio: "Short bio — training, languages, interests." },
  { name: "Team member", role: "Reception", bio: "Short bio — training, languages, interests." },
  { name: "Team member", role: "Clinic manager", bio: "Short bio — training, languages, interests." },
];

function Team() {
  return (
    <>
      <PageHero eyebrow="Our team" title="The people behind your care" intro="Doctors, nurses and staff — everyone who makes MercyMed work." />
      <section className="container-site grid gap-6 py-16 sm:grid-cols-2 lg:grid-cols-3">
        {TEAM.map((m, i) => (
          <div key={i} className="overflow-hidden rounded-2xl border bg-card">
            {m.photo ? (
              <img src={m.photo} alt={m.name} loading="lazy" className="aspect-square w-full object-cover" />
            ) : (
              <div className="flex aspect-square items-center justify-center bg-brand-gradient font-display text-5xl font-bold text-primary-foreground/80">
                {m.role[0]}
              </div>
            )}
            <div className="p-5">
              <h2 className="text-lg font-semibold">{m.name}</h2>
              <p className="text-sm font-bold text-brand-red">{m.role}</p>
              <p className="mt-2 text-sm text-muted-foreground">{m.bio}</p>
            </div>
          </div>
        ))}
      </section>
      <CtaBand />
    </>
  );
}
