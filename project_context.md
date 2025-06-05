# Project Context

## Project Overview
I'm building a task management web application for small teams. It's like a simplified Trello with real-time collaboration features. Currently in early development phase, need to set up the foundation and choose the right tools for rapid development and scalability.

## Current Stack
**Frontend:**
- Technology: React with TypeScript
- Styling: Tailwind CSS
- Build Tools: Vite

**Backend:**
- Language: Node.js with TypeScript
- Framework: Express.js
- Database: PostgreSQL

**DevOps/Infrastructure:**
- Hosting: Planning to use Vercel for frontend, Railway for backend
- Containerization: Not implemented yet
- CI/CD: GitHub Actions (basic setup)

## Current Challenges
1. Real-time updates: Need WebSocket implementation for live collaboration
2. State management: Deciding between Redux, Zustand, or React Query
3. Database design: Optimizing for team collaboration queries
4. Authentication: Setting up secure user auth and team permissions
5. Testing: No testing setup yet, need comprehensive strategy

## Goals & Next Steps
1. MVP with drag-and-drop task boards
2. Real-time collaboration features
3. User authentication and team management
4. Mobile-responsive design
5. Performance optimization for large task lists

## Team & Experience Level
**Team Size:** Solo developer
**Experience Level:** Intermediate
**Specific Areas of Expertise:** Strong in React/TypeScript, moderate in Node.js, learning DevOps

## Preferred Tools & Constraints
**Preferred Tools:**
- TypeScript: Love the type safety
- React: Already committed to the ecosystem
- PostgreSQL: Need ACID compliance for data consistency

**Tools to Avoid:**
- MongoDB: Prefer relational data for this use case
- PHP: Want to stick with JavaScript ecosystem

**Constraints:**
- Budget: Bootstrap budget, prefer free/open source with affordable paid tiers
- Platform: Must work on Linux (Ubuntu)
- Security: Need secure authentication for team data

## Specific Questions/Areas of Interest
1. Best WebSocket library for React + Node.js real-time features
2. State management for complex UI with real-time updates
3. Authentication solutions (Auth0 vs Supabase vs custom JWT)
4. Testing strategy for real-time collaborative features
5. Database optimization tools for PostgreSQL
6. Deployment and monitoring tools for small budget

## Reference URLs & Documentation
<!-- Add relevant URLs for additional context - GitHub repos, documentation, tutorials, etc. -->
**Relevant Repositories:**
- Current Project Repo: (e.g., https://github.com/yourusername/task-manager)
- Inspiration/Reference: (e.g., https://github.com/trello/trello-board)

**Documentation & Resources:**
- Framework Docs: (e.g., https://react.dev/learn, https://nodejs.org/docs)
- Deployment Guides: (e.g., https://vercel.com/docs, https://railway.app/docs)
- Learning Resources: (e.g., specific tutorials, courses, or articles you're following)

**Third-Party Services:**
- Authentication: (e.g., https://auth0.com/docs, https://supabase.io/docs/guides/auth)
- Database: (e.g., https://www.postgresql.org/docs/)
- Hosting/Cloud: (e.g., AWS documentation, Azure docs, etc.)

---
**Note:** This context helps the assistant provide targeted tool recommendations for my task management application. URLs provide additional context about your specific implementation approach and preferred documentation sources.
