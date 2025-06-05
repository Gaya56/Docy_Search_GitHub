# Example Project Context

## Project Overview
I'm building a modern e-commerce web application for small businesses. The goal is to create a scalable, secure platform that can handle product catalogs, user authentication, payment processing, and order management. Currently in the early development phase.

## Current Stack
**Frontend:**
- Technology: React 18 with TypeScript
- Styling: Tailwind CSS
- Build Tools: Vite
- State Management: Considering Redux Toolkit or Zustand

**Backend:**
- Language: Node.js with TypeScript
- Framework: Express.js (but open to alternatives)
- Database: PostgreSQL (primary), Redis (caching)
- Authentication: Considering JWT vs sessions

**DevOps/Infrastructure:**
- Hosting: Planning to use AWS or Vercel
- Containerization: Docker
- CI/CD: GitHub Actions

## Current Challenges
1. **State Management**: Deciding between Redux Toolkit vs Zustand vs React Query for complex state
2. **Database Schema**: Need help designing efficient schemas for products, orders, and inventory
3. **Payment Integration**: Looking for reliable payment processors with good developer experience
4. **Performance**: Need advice on caching strategies and database optimization
5. **Security**: Implementing proper authentication and authorization patterns

## Goals & Next Steps
1. **MVP Features**: User registration, product browsing, shopping cart, basic checkout
2. **Admin Panel**: Inventory management, order processing, analytics dashboard
3. **Mobile Responsiveness**: Ensure great mobile experience
4. **Performance Optimization**: Sub-2 second page loads
5. **Scalability**: Handle 10k+ concurrent users

## Team & Experience Level
**Team Size:** Solo developer (me) with plans to hire 1-2 developers later
**Experience Level:** Intermediate full-stack developer
**Specific Areas of Expertise:** Strong in React/JavaScript, moderate in Node.js/databases, learning DevOps

## Preferred Tools & Constraints
**Preferred Tools:**
- TypeScript: Love the type safety and developer experience
- React: Already committed and comfortable with the ecosystem
- PostgreSQL: Need reliable ACID transactions for e-commerce

**Tools to Avoid:**
- PHP: Personal preference, want to stick with JavaScript ecosystem
- MySQL: Had bad experiences with data consistency
- Vanilla CSS: Prefer utility-first approaches like Tailwind

**Constraints:**
- Budget: Bootstrap/startup budget, prefer open-source with reasonable paid tiers
- Platform: Must work well on Linux (Ubuntu) for development
- Security: E-commerce requires high security standards and PCI compliance considerations

## Specific Questions/Areas of Interest
1. **Backend Framework**: Should I stick with Express.js or consider Fastify, NestJS, or Next.js API routes?
2. **Payment Processing**: Stripe vs PayPal vs other payment processors - pros/cons?
3. **Database Tools**: Best ORMs for Node.js + PostgreSQL (Prisma vs TypeORM vs Drizzle)?
4. **Testing Strategy**: Complete testing setup for React + Node.js e-commerce app
5. **Monitoring & Analytics**: What tools for error tracking, performance monitoring, and business analytics?
6. **Security Tools**: Static analysis, vulnerability scanning, and security best practices for e-commerce

---
**Note:** This is an example context file. Replace with your actual project details!
