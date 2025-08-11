import { Link } from 'react-router-dom'
import { Github, Twitter, Linkedin, Mail } from 'lucide-react'
import { Button } from '@/components/ui/Button'

const footerLinks = {
  product: [
    { name: 'Features', href: '/features' },
    { name: 'Showcase', href: '/showcase' },
    { name: 'Pricing', href: '/pricing' },
    { name: 'Blog', href: '/blog' },
  ],
  company: [
    { name: 'About', href: '#' },
    { name: 'Contact', href: '/contact' },
    { name: 'Privacy', href: '#' },
    { name: 'Terms', href: '#' },
  ],
  social: [
    { name: 'Twitter', href: '#', icon: Twitter },
    { name: 'GitHub', href: '#', icon: Github },
    { name: 'LinkedIn', href: '#', icon: Linkedin },
    { name: 'Email', href: 'mailto:hello@example.com', icon: Mail },
  ],
}

/**
 * Site footer with navigation links, social media, and company information
 */
export function Footer() {
  return (
    <footer className="border-t border-border bg-muted/30">
      <div className="container-grid py-12">
        <div className="col-span-12 lg:col-span-6">
          <div className="space-y-4">
            <Link
              to="/"
              className="text-2xl font-bold text-gradient"
              aria-label="Go to homepage"
            >
              Brand
            </Link>
            <p className="text-muted-foreground max-w-md">
              Building exceptional digital experiences with modern technology and thoughtful design.
            </p>
            <div className="flex space-x-2">
              {footerLinks.social.map((item) => (
                <Button
                  key={item.name}
                  variant="ghost"
                  size="icon"
                  asChild
                  className="rounded-full"
                >
                  <a
                    href={item.href}
                    aria-label={item.name}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <item.icon className="h-4 w-4" />
                  </a>
                </Button>
              ))}
            </div>
          </div>
        </div>

        <div className="col-span-12 lg:col-span-6">
          <div className="grid grid-cols-2 gap-8">
            <div>
              <h3 className="font-semibold text-foreground mb-4">Product</h3>
              <ul className="space-y-3">
                {footerLinks.product.map((item) => (
                  <li key={item.name}>
                    <Link
                      to={item.href}
                      className="text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="font-semibold text-foreground mb-4">Company</h3>
              <ul className="space-y-3">
                {footerLinks.company.map((item) => (
                  <li key={item.name}>
                    <Link
                      to={item.href}
                      className="text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-border">
        <div className="container-grid py-6">
          <div className="col-span-12 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <p className="text-sm text-muted-foreground">
              © 2024 Brand. All rights reserved.
            </p>
            <p className="text-sm text-muted-foreground">
              Built with React, TypeScript & Tailwind CSS
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}