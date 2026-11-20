import { Link } from "@tanstack/react-router";
import { useState, type ReactNode } from "react";
import emblem from "@/assets/mercymed-emblem.png.asset.json";

// Edit contact details here — used across the whole site.
export const CLINIC = {
  phone: "+996 000 000 000",
  whatsapp: "996000000000",
  email: "info@mercymed.kg",
  address: "Bishkek, Kyrgyzstan",
  hours: "Mon–Fri 9:00–18:00 · Sat 9:00–14:00",
  instagram: "https://www.instagram.com/mercymed.kg",
};

const NAV = [
  { to: "/about", label: "About" },
  { to: "/services", label: "Services" },
  { to: "/corporate", label: "For organisations" },
  { to: "/education", label: "Education" },
  { to: "/team", label: "Team" },
  { to: "/outreach", label: "Mobile clinics" },
  { to: "/contact", label: "Contact" },
] as const;

export function Logo() {
  return (
    <Link to="/" className="flex items-center gap-2.5">
      <img src={emblem.url} alt="" width={36} height={36} className="h-9 w-9 rounded-sm" />
      <span className="font-display text-xl font-extrabold tracking-tight">
        <span className="text-foreground">MERCY</span>
        <span className="text-brand-red">MED</span>
      </span>
    </Link>
  );
}

export function Header() {
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-40 border-b bg-background/90 backdrop-blur">
      <div className="container-site flex h-16 items-center justify-between gap-4">
        <Logo />
        <nav className="hidden items-center gap-1 lg:flex">
          {NAV.map((n) => (
            <Link
              key={n.to}
              to={n.to}
              className="rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
              activeProps={{ className: "text-foreground bg-accent" }}
            >
              {n.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <BookButton className="hidden sm:inline-flex" />
          <button
            aria-label="Menu"
            onClick={() => setOpen(!open)}
            className="rounded-md border px-3 py-2 text-sm font-semibold lg:hidden"
          >
            {open ? "Close" : "Menu"}
          </button>
        </div>
      </div>
      {open && (
        <nav className="border-t bg-background lg:hidden">
          <div className="container-site flex flex-col py-2">
            {NAV.map((n) => (
              <Link key={n.to} to={n.to} onClick={() => setOpen(false)} className="py-3 text-base font-medium">
                {n.label}
              </Link>
            ))}
            <Link to="/contact" onClick={() => setOpen(false)} className="py-3 font-semibold text-brand-red">
              Book an appointment →
            </Link>
          </div>
        </nav>
      )}
    </header>
  );
}

export function BookButton({ className = "", label = "Book an appointment" }: { className?: string; label?: string }) {
  return (
    <Link
      to="/contact"
      className={`inline-flex items-center justify-center rounded-full bg-primary px-5 py-2.5 text-sm font-bold text-primary-foreground shadow-soft transition hover:brightness-105 ${className}`}
    >
      {label}
    </Link>
  );
}

export function GhostButton({ to, children }: { to: "/about" | "/services" | "/corporate" | "/contact" | "/team" | "/outreach"; children: ReactNode }) {
  return (
    <Link
      to={to}
      className="inline-flex items-center justify-center rounded-full border-2 border-foreground/15 px-5 py-2.5 text-sm font-bold transition hover:border-foreground/40"
    >
      {children}
    </Link>
  );
}

export function PageHero({ eyebrow, title, intro }: { eyebrow: string; title: string; intro: string }) {
  return (
    <section className="border-b bg-secondary/60">
      <div className="container-site py-16 md:py-20">
        <div className="mb-4 h-1.5 w-16 rounded-full bg-brand-gradient" />
        <p className="text-sm font-bold uppercase tracking-widest text-brand-red">{eyebrow}</p>
        <h1 className="mt-3 max-w-3xl text-4xl font-bold md:text-5xl">{title}</h1>
        <p className="mt-5 max-w-2xl text-lg text-muted-foreground">{intro}</p>
      </div>
    </section>
  );
}

export function Card({ title, children }: { title: string; children: ReactNode }) {
  return (
    <div className="rounded-2xl border bg-card p-6 transition hover:shadow-soft">
      <h3 className="text-lg font-semibold">{title}</h3>
      <div className="mt-2 text-muted-foreground">{children}</div>
    </div>
  );
}

export function CtaBand() {
  return (
    <section className="container-site py-16">
      <div className="flex flex-col items-start justify-between gap-6 rounded-3xl bg-ink p-10 text-ink-foreground md:flex-row md:items-center">
        <div>
          <h2 className="text-2xl font-bold md:text-3xl">Ready to be seen?</h2>
          <p className="mt-2 opacity-80">Request an appointment online or call us — we speak English, Kyrgyz and Russian.</p>
        </div>
        <BookButton />
      </div>
    </section>
  );
}

export function Footer() {
  return (
    <footer className="mt-auto border-t bg-muted">
      <div className="h-1.5 bg-brand-gradient" />
      <div className="container-site grid gap-10 py-12 md:grid-cols-3">
        <div>
          <Logo />
          <p className="mt-4 max-w-xs text-sm text-muted-foreground">
            Evidence-based, international medicine in Bishkek — caring for body and spirit.
          </p>
        </div>
        <div className="text-sm">
          <p className="font-semibold">Contact</p>
          <p className="mt-3 text-muted-foreground">{CLINIC.address}</p>
          <a href={`tel:${CLINIC.phone.replace(/\s/g, "")}`} className="mt-1 block text-muted-foreground hover:text-foreground">{CLINIC.phone}</a>
          <a href={`mailto:${CLINIC.email}`} className="mt-1 block text-muted-foreground hover:text-foreground">{CLINIC.email}</a>
          <p className="mt-1 text-muted-foreground">{CLINIC.hours}</p>
        </div>
        <div className="text-sm">
          <p className="font-semibold">Explore</p>
          <div className="mt-3 grid grid-cols-2 gap-1">
            {NAV.map((n) => (
              <Link key={n.to} to={n.to} className="text-muted-foreground hover:text-foreground">{n.label}</Link>
            ))}
            <a href={CLINIC.instagram} target="_blank" rel="noreferrer" className="text-muted-foreground hover:text-foreground">Instagram</a>
          </div>
        </div>
      </div>
      <div className="container-site border-t py-5 text-xs text-muted-foreground">© {new Date().getFullYear()} MercyMed Medical Center</div>
    </footer>
  );
}

export function meta(title: string, description: string) {
  const t = `${title} | MercyMed Bishkek`;
  return {
    meta: [
      { title: t },
      { name: "description", content: description },
      { property: "og:title", content: t },
      { property: "og:description", content: description },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  };
}
