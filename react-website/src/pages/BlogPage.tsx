import { SectionHeader } from '@/components/ui/SectionHeader'

export default function BlogPage() {
  return (
    <div className="min-h-screen pt-24">
      <section className="py-24">
        <div className="container-grid">
          <div className="col-span-12">
            <SectionHeader
              title="Blog"
              subtitle="Latest News"
              description="Stay updated with our latest insights and updates"
              centered
            />
          </div>
        </div>
      </section>
    </div>
  )
}