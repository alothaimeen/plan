# Project: English Language Remedial Plan Website

## 1. Project Overview

This project is a static educational website that hosts a comprehensive 4-day remedial plan for teaching English. It is designed for students at Abi Bakr Bin Al Arabi High School, under the supervision of teacher Mr. Mohammed Al-Othaimin.

The core goal is to improve students' English proficiency through an intensive, 4-day program. Students are divided into four levels based on a diagnostic test:
- **🔴 Basic (0-9 points):** Focuses on letters, basic words, and simple sentences.
- **🟡 Acceptable (10-17 points):** Focuses on building simple and complete sentences.
- **🟢 Intermediate (18-24 points):** Focuses on grammar, reading, writing, and conversation.
- **🟣 Excellent (25+ points):** These students act as **Assistant Teachers** and follow the standard school curriculum.

The website provides access to daily worksheets and short "exit ticket" tests for each level, all of which are highly optimized for printing to save paper. The main technologies are simple, static **HTML, CSS, and JavaScript**.

## 2. Key Features

- **🖨️ Print-Optimized:** All materials are designed to fit on A4 paper with minimal waste, saving 30-35% of paper.
- **✒️ Clear & Readable:** Uses specific fonts like `Comic Sans MS` and `Andika` for readability, especially for foundational levels. It also features a **Four-Line System** for handwriting practice.
- **🚀 Ready to Use:** No special setup is needed. Teachers can directly open and print materials from the browser.
- **激励 System:** A points-based system (5 points per session) is used to motivate students, which translates to participation grades.
- **🎓 Assistant Teacher Role:** Top-performing students are utilized as assistant teachers to help manage the different groups within a class. A dedicated guide (`guides/assistant-guide.html`) is provided for them.

## 3. Project Structure

The project is organized into a clear, static file structure:

- `index.html`: The main landing page where users select their proficiency level.
- `basic.html`, `acceptable.html`, `intermediate.html`, `excellent.html`: Hub pages for each of the four student levels, linking to the daily materials.
- `css/style.css`: The main stylesheet. It uses CSS variables for colors (`--color-basic`, `--color-acceptable`, etc.) to ensure a consistent look and feel.
- `js/script.js`: Contains JavaScript functions for interactivity, primarily `printAllWorksheets(level)` and `printAllTests(level)` which open multiple files at once for batch printing.
- `worksheets/`: Contains all 16 daily worksheet HTML files.
- `tests/`: Contains all 16 short test HTML files.
- `guides/`: Contains the `assistant-guide.html` for student helpers.
- `.github/workflows/pages.yml`: A GitHub Actions workflow that automatically deploys the site to GitHub Pages on every push to the `main` branch.
- **Documentation (Arabic `.md` files):** The root directory contains numerous Markdown files like `خطة_الموقع_الإلكتروني.md` (Website Plan) and `README.md`. These files document the project's plan, goals, content, and technical specifications in detail.
- **Automation Scripts (`.py`):** The project also includes several Python scripts (e.g., `merge_worksheets.py`) used during development for tasks like generating files and performing evaluations. These are not required for the live website to function.

## 4. Running & Deploying the Project

### Local Usage
To run the project locally, simply open the `index.html` file in a web browser. No web server is needed. You can use the browser's developer tools to simulate mobile views and test responsiveness.

### Deployment
The website is automatically deployed to **GitHub Pages**. The process is defined in `.github/workflows/pages.yml`. When changes are pushed to the `main` branch, the workflow uploads the entire repository as a Pages artifact and deploys it. The final URL will have a structure like: `https://<username>.github.io/<repository-name>/`.

## 5. Development Conventions

- **File Naming:** Worksheets and tests **must** follow the strict naming convention: `{level}-day{day_number}-{type}.html` (e.g., `intermediate-day3-test.html`). The JavaScript printing functions depend on this structure.
- **Adding Content:** To add new materials, create a new HTML file, ensure it is print-optimized, and place it in the appropriate directory (`worksheets/` or `tests/`). Then, link to it from the corresponding level's hub page (e.g., `intermediate.html`).
- **Styling:** All new styles should be added to `css/style.css`. Use the existing CSS variables for colors and spacing to maintain design consistency.