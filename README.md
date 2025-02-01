[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17922450)
# web-sec-2025-day-3-in-class-activity

### Collaborative Learning Activity: FastAPI RESTful API Challenge - Music Festival Management System

This activity aims to enhance your skills in designing and implementing RESTful APIs using **FastAPI** within a collaborative and competitive environment. Leveraging **GitHub Classroom** and **GitHub Codespaces**, this activity involves eight groups of four students, each tackling 32 tasks collaboratively. This structure promotes active participation and adherence to industry best practices.

---
## Music Festival Management System Scenario

**Scenario:** You are part of a development team tasked with building a RESTful API for a music festival management system. This system will be used by festival organizers, artists, and attendees to manage various aspects of the festival.

**System Requirements:**

The API should provide the following functionalities

**1. Artist Management:**

*   Add, update, and delete artist information (name, genre, country, image, etc.).
*   Retrieve artist details, including their performance schedule and stage.
*   Search for artists by name or genre.

**2. Stage Management:**

*   Add, update, and delete stage information (name, location, capacity, etc.).
*   Retrieve stage details, including the schedule of performances.

**3. Schedule Management:**

*   Create and manage the festival schedule, assigning artists to specific stages and time slots.
*   Retrieve the schedule for a specific day or stage.

**4. Ticket Management:**

*   Create and manage different ticket types (e.g., day passes, VIP tickets).
*   Allow users to purchase tickets and track their orders.
*   Generate reports on ticket sales.

**5. User Management:**

*   Allow users to create accounts and manage their profiles.
*   Implement different user roles with varying levels of access (e.g., administrator, artist, attendee).

**6. Additional Features:**

*   Implement a system for attendees to rate artists and provide feedback.
*   Integrate with a payment gateway for ticket purchases.
*   Provide real-time updates on festival news and announcements.

**Challenges:**

*   **Data Integrity:** Ensuring data consistency and accuracy across different modules.
*   **Concurrency:** Handling concurrent requests from multiple users, especially during peak times like ticket sales.
*   **Security:** Implementing robust security measures to protect user data and prevent unauthorized access.
*   **Scalability:** Designing the API to handle a large number of requests and data as the festival grows.

**Success Criteria:**

*   A fully functional API that meets the specified requirements.
*   Well-documented code and API endpoints.
*   Adherence to RESTful API design principles.
*   Efficient and scalable implementation.
*   Effective collaboration and communication within the team.

---

## Learning Objectives
1.  Design RESTful APIs following industry best practices.
2.  Implement APIs using FastAPI.
3.  Collaborate effectively in a team environment.
4.  Apply version control and collaborative coding workflows.
5.  Utilize GitHub Classroom and Codespaces for seamless collaboration.

---

## Activity Structure
1.  **Introduction and Setup**
2.  **Task Breakdown for Each Group**
3.  **Collaborative Implementation**
4.  **Competition and Evaluation**
5.  **Submission and Feedback**

---

### 1. Introduction and Setup

#### Overview:
-   Eight groups, each comprising four students, will design and implement a RESTful API for a **Music Festival Management System**.
-   Each group will complete **32 identical tasks**.
-   Tasks will be evenly distributed among group members to ensure equal contribution.
-   The objective is to complete all tasks efficiently and accurately, adhering to best practices.

#### Setup Instructions:
1.  **GitHub Classroom**:
    -   The instructor will create a GitHub Classroom assignment with eight team-based repositories (one for each group).
    -   Each group will fork the repository and work collaboratively.

2.  **GitHub Codespaces**:
    -   Each member will use GitHub Codespaces to develop and test their assigned API components.
    -   Codespaces provides a pre-configured development environment with FastAPI and all necessary dependencies installed.

3.  **Initial Setup**:
    -   Clone the repository and set up the project:
        ```bash
        git clone <repository-url>
        cd <repository-folder>
        ```
    -   Install dependencies:
        ```bash
        pip install fastapi uvicorn
        ```

4.  **Group Formation**:
    -   The instructor will form eight groups of four students each.

---

### 2. Task Breakdown for Each Group

Each group will have **32 tasks** categorized into **four domains**. Each domain contains **8 tasks**, with each group member responsible for one domain.

#### Domain 1: API Design and Documentation
1.  Define API resources.
2.  Design API endpoints .
3.  Document the API using FastAPI's built-in Swagger UI.
4.  Provide detailed descriptions for each endpoint in the Swagger UI.
5.  Implement API versioning.
6.  Incorporate error handling for invalid requests.
7.  Include examples for request and response payloads in the documentation.
8.  Create a `README.md` file with clear instructions on using the API.

#### Domain 2: Core API Implementation
1.  Implement the endpoint to retrieve all artists.
2.  Implement the endpoint to retrieve a specific artist.
3.  Implement the endpoint to add a new artist.
4.  Implement the endpoint to update an existing artist.
5.  Implement the endpoint to remove an artist.
6.  Implement the endpoint to retrieve all stages.
7.  Implement the endpoint to retrieve a specific stage.
8.  Implement the endpoint to add a new stage.

#### Domain 3: Advanced Features
1.  Implement pagination for at least 2 endpoints.
2.  Add filtering capabilities to the `GET /artists` endpoint (e.g., filter by genre or country).
3.  Implement sorting for the `GET /stages` endpoint (e.g., sort by capacity or location).
4.  Add a search feature to the `GET /artists` endpoint (e.g., search by name or genre).
5.  Implement authentication using API keys or JWT.
6.  Add rate limiting to prevent API abuse.
7.  Utilize Pydantic models for request and response validation.
8.  Write unit tests for all endpoints using `pytest`.

#### Domain 4: Deployment and Optimization
1.  Dockerize the FastAPI application.
2.  Deploy the API to a cloud platform (e.g., Heroku, AWS, or Google Cloud).
3.  Optimize API performance (e.g., implement caching with Redis).
4.  Incorporate logging to track API requests and errors.
5.  Implement health check endpoints (e.g., `GET /health`).
6.  Develop a CI/CD pipeline for automated testing and deployment.
7.  Include a `LICENSE` file in the repository.
8.  Create a `CONTRIBUTING.md` file to guide future contributors.

---

### 3. Collaborative Implementation

#### Group Collaboration:
-   Each group will utilize **GitHub Issues** to assign tasks to members.
-   Members will create feature branches for their tasks and submit pull requests for review.
-   Use **GitHub Discussions** for communication and issue resolution.

#### Example Workflow:
1.  Assign tasks using GitHub Issues: Create an issue for each task and assign it to a member.
2.  Create a feature branch:
    ```bash
    git checkout -b feature/<task-name>
    ```
3.  Commit and push changes:
    ```bash
    git add.
    git commit -m "Implemented <task-name>"
    git push origin feature/<task-name>
    ```
4.  Submit a pull request for review.

---

### 4. Competition and Evaluation

#### Competition Rules:
-   The first group to successfully complete all 32 tasks wins.
-   I will evaluate the APIs based on:
    -   **Functionality**: Does the API function as expected?
    -   **Code Quality**: Is the code clean, well-organized, and maintainable?
    -   **Best Practices**: Are industry best practices followed?
    -   **Documentation**: Is the API comprehensively documented?
    -   **Collaboration**: Did the group demonstrate effective teamwork?

#### Evaluation Criteria:
| Criteria           | Weight |
|--------------------|--------|
| Functionality      | 30%    |
| Code Quality       | 25%    |
| Best Practices     | 25%    |
| Documentation      | 10%    |
| Collaboration      | 10%    |

---

### 5. Submission and Feedback

#### Submission:
1.  Push the final code to the group's repository.
2.  Ensure all tasks are completed and documented.
3.  Submit the repository link via GitHub Classroom.

#### Feedback:
-   I will provide feedback on the API implementation.
-   The winning group will be announced, and all groups will receive constructive feedback for improvement.

---

### Additional Resources
-   [FastAPI Documentation](https://fastapi.tiangolo.com/)
-   [GitHub Classroom Guide](https://docs.github.com/en/education/manage-coursework-with-github-classroom)
-   [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)

---

By completing this activity, you will gain practical experience in designing and implementing RESTful APIs using FastAPI, while strengthening your collaborative skills in a team environment. Good luck, and may the best group win!
