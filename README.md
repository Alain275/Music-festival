web-sec-2025-day-3-in-class-activity

Collaborative Learning Activity: FastAPI RESTful API Challenge - Music Festival Management System

This activity aims to enhance your skills in designing and implementing RESTful APIs using FastAPI within a collaborative and competitive environment. Leveraging GitHub Classroom and GitHub Codespaces, this activity involves eight groups of four students, each tackling 32 tasks collaboratively. This structure promotes active participation and adherence to industry best practices.

Music Festival Management System Scenario

Scenario: You are part of a development team tasked with building a RESTful API for a music festival management system. This system will be used by festival organizers, artists, and attendees to manage various aspects of the festival.

System Requirements

The API should provide the following functionalities:

1. Artist Management:

Add, update, and delete artist information (name, genre, country, image, etc.).

Retrieve artist details, including their performance schedule and stage.

Search for artists by name or genre.

2. Stage Management:

Add, update, and delete stage information (name, location, capacity, etc.).

Retrieve stage details, including the schedule of performances.

3. Schedule Management:

Create and manage the festival schedule, assigning artists to specific stages and time slots.

Retrieve the schedule for a specific day or stage.

4. Ticket Management:

Create and manage different ticket types (e.g., day passes, VIP tickets).

Allow users to purchase tickets and track their orders.

Generate reports on ticket sales.

5. User Management:

Allow users to create accounts and manage their profiles.

Implement different user roles with varying levels of access (e.g., administrator, artist, attendee).

6. Additional Features:

Implement a system for attendees to rate artists and provide feedback.

Integrate with a payment gateway for ticket purchases.

Provide real-time updates on festival news and announcements.

Challenges

Data Integrity: Ensuring data consistency and accuracy across different modules.

Concurrency: Handling concurrent requests from multiple users, especially during peak times like ticket sales.

Security: Implementing robust security measures to protect user data and prevent unauthorized access.

Scalability: Designing the API to handle a large number of requests and data as the festival grows.

Success Criteria

A fully functional API that meets the specified requirements.

Well-documented code and API endpoints.

Adherence to RESTful API design principles.

Efficient and scalable implementation.

Effective collaboration and communication within the team.

Installation

Clone the repository:

git clone <repository_url>
cd music-festival-api

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start the FastAPI server:

uvicorn main:app --reload

API Documentation

FastAPI provides interactive API documentation with Swagger UI:

https://app.swaggerhub.com/apis/alain-ccf/fast-api/0.1.0

Deployment

The API can be deployed using render. with this endpoints(https://music-fastival.onrender.com/docs) 
A CI/CD pipeline can be configured to automate deployment and testing.CI/CD Pipeline



Automated Testing: Set up GitHub Actions for automated tests.

Continuous Deployment: Deploy to AWS/GCP/DigitalOcean using Docker.

Monitoring & Logs: Use logging tools like Prometheus and Grafana.

Contributing

Fork the repository

Create a feature branch (git checkout -b feature-name)

Commit changes (git commit -m 'Add feature')

Push to the branch (git push origin feature-name)

Open a pull request

License

This project is licensed under the GROUP 5 License.