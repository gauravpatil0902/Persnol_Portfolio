from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

skills_data = {
    "python": {
        "name": "Python",
        "icon": "fa-brands fa-python",
        "rating": 4,
        "description": "Python is my main programming language. I use it for backend development, automation, data handling, and building practical applications.",
        "learned": ["Core Python", "OOP concepts", "File handling", "Exception handling", "APIs", "Automation basics"],
        "projects": ["Portfolio backend", "Contact form with SQLite", "Web scraping practice", "Data analysis scripts"]
    },
    "django": {
        "name": "Django",
        "image": "images/django.jpg",
        "rating": 3,
        "description": "I use Django for building structured and secure backend applications with database support.",
        "learned": ["Models", "Views", "Templates", "Admin panel", "URL routing", "Database handling"],
        "projects": ["Dynamic web applications", "Backend practice projects"]
    },
    "flask": {
        "name": "Flask",
        "image": "images/flask_img.png",
        "rating": 4,
        "description": "Flask helps me create lightweight and flexible web applications using Python.",
        "learned": ["Routes", "Templates", "Forms", "SQLite integration", "Static files", "Jinja templates"],
        "projects": ["Personal portfolio", "Contact form system", "Mini web apps"]
    },
    "data-analytics": {
    "name": "Data Analytics",
    "icon": "fa-solid fa-chart-line",
    "rating": 3,
    "description": "I use data analytics concepts to understand datasets, find patterns, and create useful insights.",
    "learned": ["Data cleaning", "Data visualization", "Basic statistics", "Trend analysis"],
    "projects": ["Dataset analysis practice", "Charts and reports"]
    },
    "html": {
        "name": "HTML",
        "icon": "fa-brands fa-html5",
        "rating": 4,
        "description": "I use HTML to create clean and structured web pages.",
        "learned": ["Semantic tags", "Forms", "Tables", "Page structure", "Accessibility basics"],
        "projects": ["Portfolio pages", "Forms", "Landing sections"]
    },
    "css": {
        "name": "CSS",
        "icon": "fa-brands fa-css3",
        "rating": 4,
        "description": "I use CSS to design responsive, attractive, and modern user interfaces.",
        "learned": ["Flexbox", "Grid", "Animations", "Responsive design", "Hover effects"],
        "projects": ["Portfolio UI", "Galaxy background", "Responsive sections"]
    },
    "bootstrap": {
        "name": "Bootstrap",
        "icon": "fa-brands fa-bootstrap",
        "rating": 3,
        "description": "Bootstrap helps me build responsive layouts quickly.",
        "learned": ["Grid system", "Buttons", "Cards", "Navbar", "Responsive utilities"],
        "projects": ["Responsive web layouts", "UI practice pages"]
    },
    "sql": {
        "name": "SQL",
        "icon": "fa-solid fa-database",
        "rating": 3,
        "description": "I use SQL for storing, querying, and managing application data.",
        "learned": ["Tables", "Insert", "Select", "Update", "Delete", "SQLite basics"],
        "projects": ["Portfolio contact database", "Database practice"]
    },
    "git": {
        "name": "Git",
        "icon": "fa-brands fa-git",
        "rating": 3,
        "description": "I use Git and GitHub for version control and managing my projects.",
        "learned": ["Commit", "Push", "Pull", "Branches", "GitHub repositories"],
        "projects": ["Portfolio version control", "Project management"]
    },
    "numpy": {
        "name": "NumPy",
        "icon": "fa-solid fa-cubes",
        "rating": 3,
        "description": "I use NumPy for numerical operations and working with arrays in Python.",
        "learned": ["Arrays", "Array operations", "Mathematical functions", "Data processing basics"],
        "projects": ["Numerical computing practice"]
    },
    "pandas": {
        "name": "Pandas",
        "icon": "fa-solid fa-grip",
        "rating": 3,
        "description": "I use Pandas for data cleaning, manipulation, and analysis.",
        "learned": ["DataFrames", "CSV handling", "Filtering", "Grouping", "Cleaning data"],
        "projects": ["Dataset analysis", "CSV data projects"]
    },
    "matplotlib": {
        "name": "Matplotlib",
        "icon": "fa-solid fa-chart-column",
        "rating": 3,
        "description": "I use Matplotlib to create charts and visual reports from data.",
        "learned": ["Line charts", "Bar charts", "Pie charts", "Graph styling"],
        "projects": ["Data visualization reports", "Chart practice"]
    }
}

projects_data = {
    "ecommerce-platform": {
        "title": "Amazon-Style E-Commerce Platform",
        "image": "images/fit_2.png",
        "source": "https://github.com/gauravpatil0902/Book_Store-E-Commerce-Site",
        "description": "A Django-based polls application built with Python, HTML, CSS, and database integration. The project includes dynamic voting, question management, and user interaction features.",
        "tech_stack": ["Python", "Django", "HTML", "CSS", "SQLite/MySQL"],
        "features": ["User Registration, Login & Profile Management", "Product Catalog with 1000+ Books (Scraped Dataset)", "Advanced Search and Product Filtering", "Responsive frontend", "Shopping Cart and Wishlist Functionality"],
        "learned": ["Full-Stack Web Development with Django", "Database Design and Management", "Web Scraping and Data Processing", "Authentication and User Session Handling", "E-Commerce Application Architecture"],
        "gallery": [
            {
                "image": "images/b_home.png",
                "caption": "Amazon-inspired online bookstore with 1000+ products, smart search, cart, wishlist, and complete order management."
            },
            {
                "image": "images/cart.png",
                "caption": "Cart page where users select there Books and add to there wishlist."
            },
            {
                "image": "images/order.png",
                "caption": "Complete order management system with checkout, order tracking, status updates, and purchase history."
            }
        ]
    },
    "portfolio-site": {
        "title": "Professional Portfolio Site",
        "image": "images/port.png",
        "source": "https://github.com/gauravpatil0902/flask_projects/tree/main/portfolio_projects",
        "description": "A responsive portfolio website developed using Flask, Python, HTML, CSS, and JavaScript to showcase projects, skills, resume, and contact information professionally.",
        "tech_stack": ["Python", "Flask", "HTML", "CSS", "JavaScript", "SQLite"],
        "features": ["Animated hero section", "Contact form", "Skills carousel", "Project showcase", "Responsive layout"],
        "learned": ["Flask routes", "Jinja templates", "Canvas background", "Form handling", "Portfolio structure"],
        "gallery": [
            {
                "image": "images/port_home.png",
                "caption": "Animated portfolio home page with star background."
            },
            {
                "image": "images/skills.png",
                "caption": "Skills carousel and interactive skill detail pages."
            }
        ]
    },
    "web-scraping": {
        "title": "Web Scraping",
        "image": "images/tata.png",
        "source": "https://github.com/gauravpatil0902/-Medicine-Data-Extraction-System",
        "description": "A Python web scraping project for collecting product information such as medicine details, pricing, and structured data using BeautifulSoup and Requests.",
        "tech_stack": ["Python", "BeautifulSoup", "Requests", "Data Cleaning"],
        "features": ["Automated data extraction", "Product information collection", "Structured output", "Reusable scraping logic"],
        "learned": ["HTML parsing", "HTTP requests", "Data extraction", "Cleaning scraped data", "Automation basics"],
        "gallery": [
            {
                "image": "images/scraped_data.png",
                "caption": "Scraped data output collected from the website."
            },
            {
                "image": "images/work_flow.png",
                "caption": "Python scraping workflow using Requests and BeautifulSoup."
            }
        ]
    },
    "library-management": {
        "title": "Library Management System",
        "image": "images/lab.jpg",
        "source": "https://github.com/gauravpatil0902/Library-Management-System",
        "description": "A Django REST API project for managing library records, books, members, and issue/return operations with clean API endpoints and database-driven functionality.",
        "tech_stack": ["Python", "Django", "Django REST Framework", "SQLite/MySQL", "REST API"],
        "features": ["Book management APIs", "Member record management", "Issue and return tracking", "CRUD operations", "Database-backed API responses"],
        "learned": ["REST API development", "Django REST Framework serializers", "Model relationships", "API routing", "Backend validation"],
        "gallery": [
            {
                "image":"images/teacher.png",
                "caption": "Teacher Dashboard."
            },
            {
                "image": "images/student.png",
                "caption": "Student Dashboard."
            }
        ]
    },
    "role-based-authentication": {
        "title": "Role-Based Authentication System",
        "image": "images/rbac.png",
        "source": "https://github.com/gauravpatil0902/rbac-system-django",
        "description": "A Django REST API authentication project that manages users with different roles and permissions, allowing secure access control for protected backend resources.",
        "tech_stack": ["Python", "Django", "Django REST Framework", "Authentication", "REST API"],
        "features": ["User registration and login", "Role-based permissions", "Protected API endpoints", "User access control", "Secure backend authentication flow"],
        "learned": ["Authentication logic", "Permission classes", "Role-based access control", "API security basics", "User model handling"],
        "gallery": [
             {
                "image": "images/std.png",
                "caption": "This is Student Dashboard."
            },
            {
                "image": "images/tech.png",
                "caption": "This is Teacher Dashboard."
            }
        ]
    }
}


def save_contact_message():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    conn = sqlite3.connect("portfolio.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)

    cur.execute(
        "INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        save_contact_message()

        return redirect("/")

    return render_template("index.html")


@app.route("/about")
def about_page():
    return render_template("about-page.html")


@app.route("/<section_name>", methods=["GET", "POST"])
def section_page(section_name):
    sections = {
        "skills": "skills",
        "projects": "work",
        "education": "education",
        "contact": "contact"
    }

    if section_name == "home":
        return redirect("/")

    if section_name not in sections:
        return redirect("/")

    if request.method == "POST":
        save_contact_message()
        return redirect(request.path)

    return render_template("index.html", scroll_target=sections[section_name])


@app.route("/skill/<skill_name>")
def skill_page(skill_name):
    skill = skills_data.get(skill_name)

    if not skill:
        return redirect("/skills")

    return render_template("skill-detail.html", skill=skill)


@app.route("/project/<project_name>")
def project_page(project_name):
    project = projects_data.get(project_name)

    if not project:
        return redirect("/projects")

    return render_template("project-detail.html", project=project, project_name=project_name)


if __name__ == "__main__":
    app.run(debug=True)
