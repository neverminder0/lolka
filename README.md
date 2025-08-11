# Cutting Edge React Website

A cutting-edge, production-ready React website built with modern technologies and elegant UI design. Features smooth animations, responsive design, dark/light mode, and beautiful components.

![Website Preview](./public/og-image.jpg)

## ✨ Features

### 🎨 Design & UI
- **Glassmorphism Effects**: Beautiful glass-like components with backdrop blur
- **Smooth Animations**: Powered by Framer Motion for engaging micro-interactions
- **Dark/Light Mode**: Auto-detecting theme with smooth transitions
- **Responsive Design**: Mobile-first approach with 12-column grid system
- **Modern Aesthetic**: Large spacing, clean typography, soft shadows, subtle gradients

### 🚀 Performance
- **Lightning Fast**: Optimized with Vite build system
- **Code Splitting**: Lazy loading for routes and components
- **Tree Shaking**: Efficient bundle size with dead code elimination
- **Image Optimization**: WebP format with lazy loading
- **Critical CSS**: Inlined for faster first paint

### ♿ Accessibility
- **WCAG AA Compliant**: Proper contrast ratios and semantic HTML
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: Proper ARIA labels and roles
- **Focus Management**: Visible focus indicators

### 🔧 Developer Experience
- **Modern Stack**: React 18, Vite, Tailwind CSS, Framer Motion
- **Type Safety**: JSX with proper prop validation
- **Component Library**: Reusable, well-documented components
- **Clean Architecture**: Organized file structure and separation of concerns

## 🛠️ Tech Stack

- **Frontend**: React 18 (JSX)
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Routing**: React Router DOM
- **Icons**: Lucide React
- **Development**: ESLint, Prettier (recommended)

## 📋 Pages

1. **Home** - Hero section, features, testimonials, CTA
2. **Features** - Detailed feature showcase with integrations
3. **Showcase** - Masonry gallery with lightbox and filtering
4. **Pricing** - Monthly/yearly toggle with feature comparison
5. **Blog** - Article listing with featured posts
6. **Blog Post** - Individual article pages with related posts
7. **Contact** - Validated contact form with information
8. **404** - Beautiful error page with helpful navigation

## 🎯 Components

### Core Components
- `Button` - Versatile button with multiple variants
- `Badge` - Status indicators and tags
- `ThemeSwitch` - Animated dark/light mode toggle
- `LoadingSpinner` - Beautiful loading states

### Layout Components
- `Navbar` - Sticky navigation with blur effect
- `Footer` - Comprehensive footer with newsletter signup
- `RootLayout` - Main layout wrapper
- `SectionHeader` - Reusable section titles

### Feature Components
- `FeatureCard` - Interactive feature showcases
- `PricingCard` - Pricing tier displays
- `TestimonialCard` - Customer testimonials (via Home page)

## 🚀 Getting Started

### Prerequisites
- Node.js 16.0 or later
- npm or yarn package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cutting-edge-website
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:5173`

### Available Scripts

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build

# Linting (if configured)
npm run lint         # Run ESLint
npm run lint:fix     # Fix ESLint errors
```

## 📁 Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── Button.jsx       # Button component with variants
│   ├── Badge.jsx        # Badge/tag component
│   ├── ThemeSwitch.jsx  # Dark/light mode toggle
│   ├── Navbar.jsx       # Navigation component
│   ├── Footer.jsx       # Footer component
│   ├── SectionHeader.jsx # Section title component
│   ├── FeatureCard.jsx  # Feature showcase card
│   ├── PricingCard.jsx  # Pricing tier card
│   ├── LoadingSpinner.jsx # Loading component
│   └── RootLayout.jsx   # Main layout wrapper
├── pages/               # Page components
│   ├── Home.jsx         # Landing page
│   ├── Features.jsx     # Features page
│   ├── Showcase.jsx     # Gallery/portfolio
│   ├── Pricing.jsx      # Pricing plans
│   ├── Blog.jsx         # Blog listing
│   ├── BlogPost.jsx     # Individual blog post
│   ├── Contact.jsx      # Contact form
│   └── NotFound.jsx     # 404 error page
├── hooks/               # Custom React hooks
│   └── useTheme.jsx     # Theme management
├── utils/               # Utility functions
├── App.jsx              # Main app component
├── main.jsx             # React entry point
└── index.css            # Global styles
```

## 🎨 Customization

### Colors
The color palette is defined in `tailwind.config.js`:
- **Primary**: Purple (#7C3AED)
- **Secondary**: Cyan (#22D3EE)
- **Neutral**: Grays for text and backgrounds

### Fonts
Uses Inter font family loaded from Google Fonts. Can be customized in:
- `index.html` (font loading)
- `tailwind.config.js` (font family configuration)

### Components
All components accept standard props and can be customized via:
- `className` prop for additional Tailwind classes
- Component-specific props for behavior modification
- CSS custom properties for fine-tuning

## 📱 Responsive Design

The website is fully responsive with breakpoints:
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

All components adapt gracefully across screen sizes with:
- Fluid typography
- Flexible grid layouts
- Touch-optimized interactions
- Progressive enhancement

## ♿ Accessibility Features

- **Semantic HTML**: Proper heading structure and landmarks
- **Keyboard Navigation**: Tab order and focus management
- **Screen Readers**: ARIA labels and descriptions
- **Color Contrast**: WCAG AA compliant color combinations
- **Reduced Motion**: Respects user motion preferences

## 🔧 Performance Optimizations

### Build Optimizations
- **Code Splitting**: Pages loaded on-demand
- **Tree Shaking**: Unused code elimination
- **Asset Optimization**: Image compression and format selection
- **Bundle Analysis**: Optimized chunk sizes

### Runtime Optimizations
- **Lazy Loading**: Images and components loaded when needed
- **Memoization**: React.memo and useMemo for expensive operations
- **Virtual Scrolling**: For large lists (when implemented)
- **Service Worker**: Caching strategy (ready for implementation)

## 🌐 SEO Features

- **Meta Tags**: Comprehensive meta tag setup
- **Open Graph**: Social media sharing optimization
- **Structured Data**: Ready for schema.org implementation
- **Sitemap**: XML sitemap generation ready
- **Robots.txt**: Search engine crawler instructions

## 🔒 Security

- **Content Security Policy**: Ready for CSP headers
- **XSS Protection**: React's built-in XSS prevention
- **Dependency Scanning**: Regular security updates
- **Environment Variables**: Secure configuration management

## 🚢 Deployment

### Build for Production
```bash
npm run build
```

### Deployment Platforms
The built site can be deployed to:
- **Vercel**: Zero-config deployment
- **Netlify**: Drag-and-drop or Git integration
- **GitHub Pages**: Static site hosting
- **AWS S3**: Cloud storage hosting
- **Any static hosting service**

### Environment Variables
Create `.env.local` for environment-specific settings:
```env
VITE_APP_NAME="Your App Name"
VITE_API_URL="https://api.yourdomain.com"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the ISC License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **React Team** - For the amazing framework
- **Tailwind CSS** - For the utility-first CSS framework
- **Framer Motion** - For beautiful animations
- **Lucide** - For the beautiful icon set
- **Unsplash** - For the demo images

## 📞 Support

If you have any questions or need help with customization:

1. Check the documentation above
2. Search existing issues on GitHub
3. Create a new issue with detailed information
4. Contact support at hello@cuttingedge.com

---

**Built with ❤️ using React, Tailwind CSS, and Framer Motion**