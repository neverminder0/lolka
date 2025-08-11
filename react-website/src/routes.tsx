import { lazy } from 'react'
import { createBrowserRouter } from 'react-router-dom'
import { RootLayout } from './layouts/RootLayout'
import { PageSuspense } from './components/ui/PageSuspense'

// Lazy load all pages for better performance
const HomePage = lazy(() => import('./pages/HomePage'))
const FeaturesPage = lazy(() => import('./pages/FeaturesPage'))
const ShowcasePage = lazy(() => import('./pages/ShowcasePage'))
const PricingPage = lazy(() => import('./pages/PricingPage'))
const BlogPage = lazy(() => import('./pages/BlogPage'))
const BlogPostPage = lazy(() => import('./pages/BlogPostPage'))
const ContactPage = lazy(() => import('./pages/ContactPage'))
const NotFoundPage = lazy(() => import('./pages/NotFoundPage'))

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    errorElement: <PageSuspense><NotFoundPage /></PageSuspense>,
    children: [
      {
        index: true,
        element: <PageSuspense><HomePage /></PageSuspense>,
      },
      {
        path: 'features',
        element: <PageSuspense><FeaturesPage /></PageSuspense>,
      },
      {
        path: 'showcase',
        element: <PageSuspense><ShowcasePage /></PageSuspense>,
      },
      {
        path: 'pricing',
        element: <PageSuspense><PricingPage /></PageSuspense>,
      },
      {
        path: 'blog',
        element: <PageSuspense><BlogPage /></PageSuspense>,
      },
      {
        path: 'blog/:slug',
        element: <PageSuspense><BlogPostPage /></PageSuspense>,
      },
      {
        path: 'contact',
        element: <PageSuspense><ContactPage /></PageSuspense>,
      },
      {
        path: '*',
        element: <PageSuspense><NotFoundPage /></PageSuspense>,
      },
    ],
  },
])