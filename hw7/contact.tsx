import { createFileRoute } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { PageHero, CLINIC, meta } from "@/components/site";

export const Route = createFileRoute("/contact")({
  head: () => meta("Book an appointment & contact", "Request an appointment at MercyMed in Bishkek, or contact us by phone, WhatsApp or email."),
  component: Contact,
});

const field = "mt-1 w-full rounded-lg border bg-card px-4 py-3 text-base outline-none focus:ring-2 focus:ring-ring";

function Contact() {
  const [sent, setSent] = useState(false);
  function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const text = [
      "Appointment request — MercyMed website",
      `Name: ${f.get("name")}`,
      `Phone: ${f.get("phone")}`,
      `Service: ${f.get("service")}`,
      `Preferred date: ${f.get("date") || "any"}`,
      `Language: ${f.get("lang")}`,
      `Message: ${f.get("message") || "-"}`,
    ].join("\n");
    window.open(`https://wa.me/${CLINIC.whatsapp}?text=${encodeURIComponent(text)}`, "_blank");
    setSent(true);
  }

  return (
    <>
      <PageHero eyebrow="Contact" title="Book an appointment" intro="Fill in the form and send it to us on WhatsApp — we'll confirm your time. Or simply call." />
      <section className="container-site grid gap-12 py-16 md:grid-cols-[1.4fr_1fr]">
        <form onSubmit={submit} className="grid gap-4 rounded-2xl border bg-card p-6 sm:grid-cols-2">
          <label className="text-sm font-semibold">Full name<input required name="name" className={field} /></label>
          <label className="text-sm font-semibold">Phone<input required name="phone" type="tel" className={field} /></label>
          <label className="text-sm font-semibold">Service
            <select name="service" className={field}>
              <option>Consultation</option><option>Laboratory tests</option><option>Check-up</option>
              <option>Vaccination</option><option>Corporate / organisation</option><option>Other</option>
            </select>
          </label>
          <label className="text-sm font-semibold">Preferred date<input name="date" type="date" className={field} /></label>
          <label className="text-sm font-semibold sm:col-span-2">Language
            <select name="lang" className={field}><option>English</option><option>Кыргызча</option><option>Русский</option></select>
          </label>
          <label className="text-sm font-semibold sm:col-span-2">Message<textarea name="message" rows={4} className={field} /></label>
          <button className="rounded-full bg-primary px-6 py-3 font-bold text-primary-foreground shadow-soft sm:col-span-2">Send request via WhatsApp</button>
          {sent && <p className="text-sm text-muted-foreground sm:col-span-2">Thank you! If WhatsApp didn't open, please call us at {CLINIC.phone}.</p>}
        </form>
        <div className="space-y-6">
          <div><p className="text-sm font-bold uppercase tracking-widest text-brand-red">Call</p><a href={`tel:${CLINIC.phone.replace(/\s/g, "")}`} className="text-2xl font-bold">{CLINIC.phone}</a></div>
          <div><p className="text-sm font-bold uppercase tracking-widest text-brand-red">Email</p><a href={`mailto:${CLINIC.email}`} className="text-lg">{CLINIC.email}</a></div>
          <div><p className="text-sm font-bold uppercase tracking-widest text-brand-red">Address</p><p className="text-lg">{CLINIC.address}</p></div>
          <div><p className="text-sm font-bold uppercase tracking-widest text-brand-red">Hours</p><p className="text-lg">{CLINIC.hours}</p></div>
          <iframe title="Map" className="h-56 w-full rounded-2xl border" loading="lazy" src="https://www.google.com/maps?q=Bishkek&output=embed" />
        </div>
      </section>
    </>
  );
}
