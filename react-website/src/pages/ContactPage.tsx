import { SectionHeader } from '@/components/ui/SectionHeader'

export default function ContactPage() {
  return (
    <div className="min-h-screen pt-24">
      <section className="py-24">
        <div className="container-grid">
          <div className="col-span-12">
            <SectionHeader
              title="Contact Us"
              subtitle="Get In Touch"
              description="We'd love to hear from you"
              centered
            />
          </div>
        </div>
      </section>
    </div>
  )
}