import { SectionHeader } from '@/components/ui/SectionHeader'

export default function ShowcasePage() {
  return (
    <div className="min-h-screen pt-24">
      <section className="py-24">
        <div className="container-grid">
          <div className="col-span-12">
            <SectionHeader
              title="Showcase"
              subtitle="Our Work"
              description="Explore our portfolio of amazing projects"
              centered
            />
          </div>
        </div>
      </section>
    </div>
  )
}