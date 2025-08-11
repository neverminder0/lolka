import { SectionHeader } from '@/components/ui/SectionHeader'

export default function BlogPostPage() {
  return (
    <div className="min-h-screen pt-24">
      <section className="py-24">
        <div className="container-grid">
          <div className="col-span-12">
            <SectionHeader
              title="Blog Post"
              subtitle="Article"
              description="Read our latest article"
              centered
            />
          </div>
        </div>
      </section>
    </div>
  )
}