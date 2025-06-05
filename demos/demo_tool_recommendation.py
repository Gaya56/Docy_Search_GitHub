#!/usr/bin/env python3
"""
Demo script for the Tool Recommendation System
This demonstrates the system capabilities with mock data when API keys are not available
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def mock_brave_search_results():
    """Mock Brave search results for demonstration"""
    return """Search Results for 'web development framework' (Category: web):

1. **React - A JavaScript library for building user interfaces**
   URL: https://reactjs.org/
   Description: React is a free and open-source front-end JavaScript library for building user interfaces based on components.

2. **Vue.js - The Progressive JavaScript Framework**
   URL: https://vuejs.org/
   Description: Vue.js is an open-source model–view–viewmodel front end JavaScript framework for building user interfaces and single-page applications.

3. **Angular - Platform for building mobile and desktop web applications**
   URL: https://angular.io/
   Description: Angular is a TypeScript-based free and open-source web application framework led by the Angular Team at Google.

4. **Next.js - The React Framework for Production**
   URL: https://nextjs.org/
   Description: Next.js is a React framework that gives you building blocks to create web applications with server-side rendering and static site generation.

5. **Svelte - Cybernetically enhanced web apps**
   URL: https://svelte.dev/
   Description: Svelte is a free and open-source front end compiler created by Rich Harris and maintained by the Svelte core team members.

6. **Express.js - Fast, unopinionated, minimalist web framework for Node.js**
   URL: https://expressjs.com/
   Description: Express.js is a back end web application framework for building RESTful APIs with Node.js.

7. **Django - The web framework for perfectionists with deadlines**
   URL: https://www.djangoproject.com/
   Description: Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.

8. **Laravel - The PHP Framework for Web Artisans**
   URL: https://laravel.com/
   Description: Laravel is a web application framework with expressive, elegant syntax for PHP developers."""

def mock_ai_analysis():
    """Mock AI analysis results for demonstration"""
    return """# Tool Analysis and Recommendations

Based on the search results for web development frameworks, here are my top 5 recommendations ranked by relevance, reliability, and ease of use:

## Top 5 Recommended Tools

### 1. **React** - Score: 9.5/10
- **Relevance**: Perfect for modern frontend development
- **Reliability**: Backed by Meta, extremely mature ecosystem
- **Installation**: Easy (via Create React App or Vite)
- **Key Features**: Component-based architecture, virtual DOM, huge ecosystem
- **Use Cases**: Single-page applications, complex UIs, mobile apps (React Native)
- **Concerns**: Learning curve for beginners, frequent ecosystem changes

### 2. **Next.js** - Score: 9.2/10
- **Relevance**: Excellent for full-stack React applications
- **Reliability**: Production-ready with excellent performance optimizations
- **Installation**: Easy (single command setup)
- **Key Features**: Server-side rendering, static site generation, API routes
- **Use Cases**: E-commerce, blogs, enterprise applications
- **Concerns**: Opinionated structure, vendor lock-in considerations

### 3. **Vue.js** - Score: 8.8/10
- **Relevance**: Great balance of simplicity and power
- **Reliability**: Mature framework with strong community
- **Installation**: Easy (CDN or CLI)
- **Key Features**: Progressive adoption, excellent documentation, TypeScript support
- **Use Cases**: Prototyping, enterprise applications, gradual migration from jQuery
- **Concerns**: Smaller ecosystem compared to React, fewer job opportunities

### 4. **Django** - Score: 8.5/10
- **Relevance**: Excellent for backend development and full-stack Python apps
- **Reliability**: Battle-tested framework used by major companies
- **Installation**: Medium (requires Python environment setup)
- **Key Features**: Admin interface, ORM, security features, rapid development
- **Use Cases**: Content management, data-driven applications, REST APIs
- **Concerns**: Can be overkill for simple applications

### 5. **Express.js** - Score: 8.3/10
- **Relevance**: Essential for Node.js backend development
- **Reliability**: Minimalist but stable, widely adopted
- **Installation**: Easy (npm install)
- **Key Features**: Lightweight, flexible, extensive middleware ecosystem
- **Use Cases**: REST APIs, microservices, real-time applications
- **Concerns**: Requires additional libraries for full functionality

## Reasoning for Rankings

**Top Choice (React)**: Largest ecosystem, excellent job market, component reusability makes it valuable long-term investment.

**Full-Stack Solution (Next.js)**: Production-ready React with built-in optimizations, perfect for modern web applications.

**Beginner-Friendly (Vue.js)**: Gentle learning curve with excellent documentation, great for getting started quickly.

**Python Backend (Django)**: Comprehensive framework with batteries included, excellent for data-driven applications.

**Node.js Foundation (Express.js)**: Essential building block for JavaScript backend development.

## Workflow Recommendation

For beginners:
1. Start with Vue.js for frontend fundamentals
2. Learn Express.js for backend basics
3. Progress to React for career advancement

For intermediate developers:
1. Choose React + Next.js for modern full-stack development
2. Use Django for Python-based applications
3. Combine Express.js with React for custom solutions

For advanced developers:
1. Build custom toolchains combining multiple frameworks
2. Consider micro-frontends with React
3. Implement serverless architectures with Next.js"""

def mock_installation_guide():
    """Mock installation guide for demonstration"""
    return """# Installation Guide: Node.js (linux)

## Prerequisites and System Requirements

- **Operating System**: Linux (Ubuntu, Debian, CentOS, Fedora, Arch Linux)
- **Memory**: Minimum 512MB RAM (2GB+ recommended for development)
- **Disk Space**: 200MB for Node.js installation
- **Network**: Internet connection for npm packages
- **Privileges**: Root/sudo access for system-wide installation

## Step-by-Step Installation Instructions

### Method 1: Package Manager Installation (Recommended)

#### Ubuntu/Debian:
```bash
# Update package list
sudo apt update

# Install Node.js and npm
sudo apt install nodejs npm

# Verify installation
node --version
npm --version
```

#### CentOS/RHEL/Fedora:
```bash
# For CentOS/RHEL 7+
sudo yum install nodejs npm

# For CentOS/RHEL 8+ and Fedora
sudo dnf install nodejs npm

# Verify installation
node --version
npm --version
```

#### Arch Linux:
```bash
# Install Node.js and npm
sudo pacman -S nodejs npm

# Verify installation
node --version
npm --version
```

### Method 2: NodeSource Repository (Latest LTS)

```bash
# Ubuntu/Debian - Add NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# CentOS/RHEL/Fedora - Add NodeSource repository
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo yum install -y nodejs

# Verify installation
node --version
npm --version
```

### Method 3: Node Version Manager (NVM)

```bash
# Install NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload bash profile
source ~/.bashrc

# Install latest LTS Node.js
nvm install --lts
nvm use --lts

# Verify installation
node --version
npm --version
```

## Post-Installation Verification Steps

1. **Basic functionality test**:
   ```bash
   node -v
   npm -v
   ```

2. **Create a simple test file**:
   ```bash
   echo 'console.log("Hello, Node.js!");' > test.js
   node test.js
   ```

3. **Test npm package installation**:
   ```bash
   npm init -y
   npm install express
   ```

4. **Check global npm packages location**:
   ```bash
   npm root -g
   ```

## Common Troubleshooting Tips

### Issue: "EACCES" permission errors with npm
**Solution**: Configure npm to use a different directory:
```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### Issue: Node.js version conflicts
**Solution**: Use NVM to manage multiple versions:
```bash
nvm list
nvm use 18.19.0  # Switch to specific version
```

### Issue: Slow npm installations
**Solution**: Use npm cache and parallel installations:
```bash
npm cache clean --force
npm install --prefer-offline
```

### Issue: Module not found errors
**Solution**: Check NODE_PATH and reinstall node_modules:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Configuration Recommendations

### 1. Set up global npm packages directory:
```bash
# Create global directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'

# Add to PATH in ~/.bashrc
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
```

### 2. Configure npm for faster installations:
```bash
# Set registry to use faster mirror (optional)
npm config set registry https://registry.npmjs.org/

# Enable parallel downloads
npm config set maxsockets 20
```

### 3. Install essential global packages:
```bash
# Install commonly used global packages
npm install -g nodemon
npm install -g pm2
npm install -g http-server
npm install -g create-react-app
```

### 4. Basic package.json setup:
```bash
# Initialize new project
npm init -y

# Install common dependencies
npm install express dotenv cors helmet
npm install -D nodemon jest eslint
```

## Advanced Features Setup

### Project Structure:
```bash
# Create standard Node.js project structure
mkdir my-node-app
cd my-node-app
npm init -y
mkdir src tests docs
touch src/index.js README.md .gitignore
```

### Environment Configuration:
```bash
# Install dotenv for environment variables
npm install dotenv

# Create .env file
echo "NODE_ENV=development" > .env
echo "PORT=3000" >> .env
```

### Development Tools:
```bash
# Install development dependencies
npm install -D nodemon eslint prettier
npm install -D jest supertest  # for testing
```

## Integration with Other Tools

- **With React**: Use Create React App or Next.js
- **With Databases**: Install drivers (mysql2, pg, mongodb)
- **With Docker**: Create Dockerfile for containerization
- **With PM2**: Process manager for production deployment
- **With Express**: Web framework for building APIs

Node.js is now successfully installed and ready for JavaScript development!

## Prerequisites and System Requirements

- **Operating System**: Linux (Ubuntu, Debian, CentOS, Fedora, Kali Linux)
- **Memory**: Minimum 512MB RAM (2GB+ recommended for large scans)
- **Disk Space**: 50MB for basic installation
- **Network**: Internet connection for updates and script downloads
- **Privileges**: Root/sudo access for advanced scanning features

## Step-by-Step Installation Instructions

### Method 1: Package Manager Installation (Recommended)

#### Ubuntu/Debian:
```bash
# Update package list
sudo apt update

# Install nmap
sudo apt install nmap

# Verify installation
nmap --version
```

#### CentOS/RHEL/Fedora:
```bash
# For CentOS/RHEL 7+
sudo yum install nmap

# For CentOS/RHEL 8+ and Fedora
sudo dnf install nmap

# Verify installation
nmap --version
```

#### Arch Linux:
```bash
# Install nmap
sudo pacman -S nmap

# Verify installation
nmap --version
```

### Method 2: Source Compilation

```bash
# Install build dependencies (Ubuntu/Debian)
sudo apt install build-essential libssl-dev

# Download latest source
wget https://nmap.org/dist/nmap-7.94.tar.bz2
tar -xjf nmap-7.94.tar.bz2
cd nmap-7.94

# Configure and compile
./configure
make
sudo make install

# Verify installation
nmap --version
```

### Method 3: Snap Package

```bash
# Install via snap
sudo snap install nmap

# Verify installation
nmap --version
```

## Post-Installation Verification Steps

1. **Basic functionality test**:
   ```bash
   nmap -v
   ```

2. **Local scan test**:
   ```bash
   nmap 127.0.0.1
   ```

3. **Check script database**:
   ```bash
   nmap --script-updatedb
   ls /usr/share/nmap/scripts/ | head -10
   ```

4. **Test privilege escalation** (for advanced features):
   ```bash
   sudo nmap -sS 127.0.0.1
   ```

## Common Troubleshooting Tips

### Issue: "Permission denied" errors
**Solution**: Use sudo for SYN scans and OS detection:
```bash
sudo nmap -sS -O target_ip
```

### Issue: Slow scanning performance
**Solution**: Adjust timing and parallelism:
```bash
nmap -T4 --min-parallelism 100 target_ip
```

### Issue: Firewall blocking scans
**Solution**: Use different scan techniques:
```bash
nmap -sT -Pn target_ip  # TCP connect scan, skip ping
```

### Issue: Scripts not found
**Solution**: Update script database:
```bash
sudo nmap --script-updatedb
```

## Configuration Recommendations

### 1. Create alias for common scans:
```bash
# Add to ~/.bashrc or ~/.zshrc
alias nmapquick='nmap -T4 -F'
alias nmapfull='nmap -T4 -A -v'
alias nmaptcp='nmap -sS -O -sV'
```

### 2. Set up custom scan profiles:
```bash
# Create ~/.nmap directory for custom scripts
mkdir ~/.nmap
```

### 3. Configure output directory:
```bash
# Create directory for scan results
mkdir ~/nmap_results
```

### 4. Basic security scanning command:
```bash
# Comprehensive security scan
nmap -sS -sV -sC -O -A --script vuln target_ip
```

## Advanced Features Setup

### NSE (Nmap Scripting Engine):
```bash
# List available scripts
nmap --script-help all | grep -E '^[a-z]' | head -20

# Run vulnerability scripts
nmap --script vuln target_ip

# Run discovery scripts
nmap --script discovery target_ip
```

### Performance Optimization:
```bash
# Fast scan with service detection
nmap -T4 -F -sV target_ip

# Aggressive scan (fast but more detectable)
nmap -T4 -A target_ip
```

## Integration with Other Tools

- **With Metasploit**: Use nmap XML output for target import
- **With Burp Suite**: Feed discovered web services to Burp
- **With Nuclei**: Use nmap results to identify services for Nuclei templates
- **With OpenVAS**: Import nmap scan results for comprehensive assessment

Nmap is now successfully installed and ready for network discovery and security auditing!"""

def demonstrate_features():
    """Demonstrate the tool recommendation system features"""
    print("🎯 Tool Recommendation System Demo")
    print("=" * 50)
    
    print("\n1. 🔍 TOOL SEARCH SIMULATION")
    print("Query: 'web development framework' (Category: web)")
    print("\nResults:")
    print(mock_brave_search_results())
    
    print("\n" + "="*50)
    print("\n2. 🤖 AI ANALYSIS SIMULATION")
    print("Analyzing search results with AI ranking...")
    print(mock_ai_analysis())
    
    print("\n" + "="*50)
    print("\n3. 📋 INSTALLATION GUIDE SIMULATION")
    print("Generating installation guide for top recommendation...")
    print(mock_installation_guide())
    
    print("\n" + "="*50)
    print("\n🎉 DEMO COMPLETE!")
    print("\nThe tool recommendation system provides:")
    print("✅ Live web search for current tools")
    print("✅ AI-powered analysis and ranking")
    print("✅ Comprehensive installation guides")
    print("✅ Task-specific recommendations")
    print("✅ Tool comparison capabilities")
    print("\nTo use with real data, add your API keys to .env file:")
    print("- BRAVE_API_KEY (for search)")
    print("- GOOGLE_API_KEY (for AI analysis)")

if __name__ == "__main__":
    demonstrate_features()
