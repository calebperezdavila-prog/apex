# 📊 Apex Spend — Premium Fintech Dashboard PWA

Apex Spend is a high-performance, ultra-premium Fintech Personal Finance tracker and Progressive Web App (PWA). It features a beautiful, glassmorphic dark-theme UI with fluid micro-animations, interactive SVG/Canvas charting, and a robust, server-persisted Python Flask backend.

---

## ✨ Features

### 🎨 Modern Glassmorphic Design System
- **Obsidian Theme**: Sleek, deep dark mode design (`#05070a` base) utilizing harmonized HSL color tokens.
- **Ambient Glow**: Interactive background spheres that drift dynamically using CSS keyframe animations.
- **Unified Modals**: 100% custom prompt and confirmation modal overlays matching the glassmorphic theme (no generic browser alerts or prompts).
- **Responsive Fluid Layout**: Premium grid system scaling fluidly to support desktop, tablet, and mobile browsers.

### 📈 Visual Intelligence & Charts
- **Budget Health Progress Ring**: Circular SVG indicator tracking real-time budget consumption. Displays a predictive budget burndown warning showing if and when you're on track to exceed your limit.
- **Category Allocation Donut**: Segmented SVG donut chart with interactive hover focuses that dynamically updates values and legend distributions.
- **Spending Velocity Spline**: High-fidelity SVG coordinate chart plotting cumulative daily outflows with a hover-focused tooltip displaying precise data points.
- **Intensity Heatmap Grid**: Activity grid plotting day-by-day spending intensity. Clicking a cell instantly isolates and filters the ledger to that day's transactions!

### 💼 Smart Ledger Management
- **Instant Search & Sort**: Fuzzy search across descriptions and tags, with sorting by Newest, Oldest, Highest, and Lowest amounts.
- **Tagging Engine**: Support for multi-tagging transactions with colored tag badges.
- **Optimistic Soft Deletions**: Deleting transactions happens instantly on the UI, displaying a 5-second "Undo" toast before executing background API requests.
- **Bulk Operations**: Seamless toggle mode for selecting and batch-deleting multiple entries.
- **Quick-Add Chips**: Lightning-fast quick chips for common daily purchases.
- **Report Modals**: In-depth monthly category reports showing breakdown ratios and printable reports.

### ⚙️ Automation & Limits
- **Recurring Bills Engine**: Automated bill scheduler that logs repeating expenses (weekly, monthly, yearly) on their billing dates.
- **Savings Goal Tracker**: Interactive widget tracking a monthly savings target.
- **Per-Category Caps**: Customizable warning limits for individual categories with custom push toasts on approaching or exceeding budgets.

---

## 🛠️ Architecture & Backend

The project is structured with clean separation of concerns:
- **Backend (`app.py`)**: Lightweight Python Flask REST API managing database updates and hosting static assets.
- **Database (`data/data.json`)**: Persistent JSON store featuring automatic dynamic key migration for pre-existing user records.
- **Frontend (`static/js/main.js` & `static/css/style.css`)**: Vanilla JavaScript rendering engine and a custom CSS variable design system.
- **PWA Capabilities (`sw.js` & `manifest.json`)**: Service worker caching and metadata enabling full desktop and mobile installation.

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Install Flask
Open your terminal and install the Flask dependency:
```bash
pip install Flask
```

### 3. Run the Application
Navigate to the project root directory and start the local web server:
```bash
python app.py
```

The application will launch in debug mode and be available at:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📦 Project Structure

```
apex-spend/
├── app.py                  # Python Flask Server & API Routes
├── data/
│   └── data.json           # Local JSON Database (Ignored by Git)
├── templates/
│   └── index.html          # High-Fidelity UI Layout
├── static/
│   ├── css/
│   │   └── style.css       # Design Tokens & Layout Rules
│   ├── js/
│   │   └── main.js         # Interactive State & SVG Rendering
│   ├── icon.svg            # PWA Vector Icon Graphics
│   ├── manifest.json       # PWA Application Metadata
│   └── sw.js               # Service Worker Caching Script
└── .gitignore              # Git Ignore Safeguards
```

---

## 🔒 License
This project is licensed under the MIT License.
