# Social Networking API
 
This project is a social networking API built using Django Rest Framework (DRF). It provides core functionalities for user management, searching, and handling friend requests.
 
## Features
 
- **User Registration and Authentication**
  - User signup with email and password.
  - User login with email and password (case insensitive).
  - Token-based authentication for secure API access.
 
- **Search Functionality**
  - Search for users by email or name (partial matching supported).
  - Pagination support with up to 10 records per page.
 
- **Friend Request Management**
  - Send friend requests to other users.
  - Accept or reject friend requests.
  - List of friends (accepted friend requests).
  - View pending friend requests (requests received but not yet accepted or rejected).
  - Rate limiting to prevent sending more than 3 friend requests within a minute.
 
## Technology Stack
 
- **Backend Framework**: Django with Django Rest Framework
- **Database**: PostgreSQL
- **Authentication**: Token-based authentication (DRF's TokenAuthentication)
- **Containerization**: Docker and Docker Compose
 
## Installation
 
### Prerequisites
 
- Docker
- Docker Compose
 
### Steps
 
1. **Clone the repository**:
    ```bash
git clone https://github.com/NithinKrishna10/social_network.git
    cd social-network-api
    ```
 
2. **Set up environment variables**:
 
   Create a `.env` file in the root directory with the following content:
   ```dotenv
   POSTGRES_DB=your_db_name
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   DJANGO_SECRET_KEY=your_secret_key
   DJANGO_DEBUG=True

