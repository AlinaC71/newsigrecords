# 🗂️ SigRec — Flask App
A web application DMS (Document Management System) built with Flask and SQlite. It aims to streamline and automate the document management process, replacing the manual workflows typically used in managing signalling design documents.

## 🚀 Live Demo

🔗 [View the live app here](https://newsigrecords.onrender.com)

---

## 🧰 Tech Stack

- **Flask** — Web framework (Python)
- **SQLite** — Lightweight relational database
- **SQLAlchemy** — ORM for database interaction
- **Bootstrap 5** — UI styling and responsiveness
- **Jinja2** — Templating engine
- **Render** — Cloud deployment

---

## 📌 Key Features & Highlights

- Built for Safety-Critical Workflows
Designed to support industry-specific, safety-critical processes with built-in alert notifications to help reduce errors and ensure compliance.

- Real-Time Record Control & Versioning
Maintains up-to-date record availability and status tracking, while enforcing strict version control in line with industry standards.

- Modular Application Design
Follows the Flask application factory pattern (create_app()) to ensure scalability and modular development.

- Focused Functional Scope
The Record Control section is currently the only fully implemented module — it is the most complex, and its architecture will be reused and adapted for other planned sections like Design and Management.

- Database Migration
Originally developed with MySQL, the application was later converted to SQLite for simplified local development and deployment.

- Production Deployment via Render
Deployed on Render with secure environment variable management and persistent database support.


## 🚧 Planned Improvements
- Full Module Implementation
Extend the current architecture to fully implement the Design and Management modules, building on the existing Record Control foundation.

- Role-Based Access Control (RBAC)
Add a login and authentication system to support role-specific access for different user groups, including: Design team, 
Record Control team, Management and Database administrators

- Migration to PostgreSQL
Migrate from SQLite to PostgreSQL for improved data integrity, scalability, and multi-user concurrency, especially for production use where persistent and transaction-safe storage is essential.




