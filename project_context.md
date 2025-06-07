### Project Summary

We’re building a simple, responsive website for a custom "Sona" business. Clients can upload or take a photo of the space where they want their Sona (e.g., a mural or artwork), then use an interactive builder to design and place their own Sona in that space. As they adjust style, size, and options, they see live price updates. The site must work seamlessly on phones, tablets, and desktops.

Edited Prompt Document

### Overview

We want to build a user-friendly web application that lets customers create custom Sonas (visual art pieces) by uploading or photographing their target space. The key features include real-time design, seamless photo capture on any device, and dynamic price calculation as clients customize their Sonas.

### Technical Requirements

#### Frontend:

- Framework: React + TypeScript or Vue.js
- Responsive styling: Tailwind CSS or Bootstrap
- Photo capture and upload: HTML5 file input with image capture and fallback file picker
- Interactive builder: Canvas or WebGL component to place and adjust the Sona preview
- Live price updates: React state or Vue reactivity to recalculate price on changes

Backend:

Language: Node.js with TypeScript or Python (FastAPI)

#### Backend:

- Language: Node.js with TypeScript or Python (FastAPI)
- Framework: Express.js (Node) or FastAPI (Python)
- Database: PostgreSQL for orders and design presets
- Image processing: Sharp (Node) or Pillow (Python) to resize and process client photos

Backend: Railway, Heroku, or AWS Elastic Beanstalk

Storage: AWS S3 or Cloudinary for uploaded images
#### DevOps/Hosting:

- Frontend: Vercel or Netlify
- Backend: Railway, Heroku, or AWS Elastic Beanstalk
- Storage: AWS S3 or Cloudinary for uploaded images
- CI/CD: GitHub Actions for automated builds and deployments
Performance & Scalability: Optimize image processing pipelines and caching to handle many concurrent users without lag.

User Authentication & Orders: Secure client accounts, save projects in progress, and manage checkout flow.

### Key Challenges

- **Cross-Device Photo Capture:** Ensure the upload component works reliably on mobile cameras and desktop file pickers.
- **Real-Time Preview & Pricing:** Implement an efficient canvas-based preview component that reflects design changes instantly and triggers price recalculation.
- **Performance & Scalability:** Optimize image processing pipelines and caching to handle many concurrent users without lag.
- **User Authentication & Orders:** Secure client accounts, save projects in progress, and manage checkout flow.

Test on multiple devices (iOS, Android, desktop) to verify photo capture and preview functionality.

### Next Steps

1. Prototype the photo upload + canvas preview feature in a sandbox React app.
2. Build a pricing engine service that calculates cost based on dimensions, materials, and options.
3. Design database schema for storing projects, users, and orders.
4. Set up basic UI routing and authentication flow.
5. Test on multiple devices (iOS, Android, desktop) to verify photo capture and preview functionality.
