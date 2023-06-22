<img src="assets/partnerup_logo.png" alt="PartnerUp Logo" width="400px">

# PartnerUp

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Content 📋
- [Introduction](#introduction-🖋️)
- [Installation](#installation-🔽)
- [Usage](#usage-🎯)
- [Getting Started](#getting-started-🌠)
- [Demo](#demo-📹)
- [Technologies](#technologies-🧑‍💻)
- [APIs and Methods](#apis-and-methods-🔑)
- [Future Features](#future-features-📇)
- [Known Bugs](#known-bugs-🐛)
- [Contributing](#contributing-🔼)
- [License](#license-📋)
- [Authors](#authors)
- [Acknowledgement](#acknowledgement)

## Introduction 🖋️
PartnerUp is a web application designed to address the challenges faced by ALX students in finding suitable project partners.
We understand that collaborating on projects can be a daunting task, with students often struggling to find compatible partners who share their coding style and work ethic.
This can lead to frustration, unproductive experiences, and subpar project outcomes.

The mission is to simplify the process of finding project partners by leveraging the power of the GitHub platform.
PartnerUp provides a seamless login experience, allowing users to authenticate themselves with their GitHub credentials.
Once logged in, users gain access to a range of features and tools to enhance their project collaboration.

Our web application is specifically designed for ALX students, providing them with a dedicated platform to connect with potential project partners.
PartnerUp is accessible to every student with a GitHub account and an internet connection, regardless of their location.
By bringing students together and fostering productive collaborations, we believe PartnerUp will contribute to the growth and success of ALX students in their software engineering journey.

PartnerUp is more than just a project partner matching service.
It's a community-driven platform that aims to empower students, enhance project outcomes, and cultivate a culture of originality and collaboration.
Join us on this exciting journey, log in with your GitHub account, and revolutionize the way you find project partners at ALX!

**[Visit PartnerUp](https://partnerup.pelumi.tech)**

For more details about the motivation and features of PartnerUp, please refer to our [blog](https://dev.to/ajipelumi/partnerup-revolutionizing-project-collaboration-4bkj).

## Installation 🔽
1. Clone the repository: `git clone https://github.com/ajipelumi/partnerup.git`
2. Navigate to the project directory: `cd partnerup`
3. Install the necessary dependencies:
   - Open the `config` directory: `cd config`
   - Run the dependency installation script: `bash install_dependencies.sh`
   - This script will install the required dependencies for the project.
4. Configure Nginx:
   - Copy the Nginx configuration file to the appropriate location: `sudo cp nginx_config /etc/nginx/sites-available/default`
   - Enable the site: `sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default`
   - Restart Nginx: `sudo service nginx restart`
   - Nginx will now be configured to serve the PartnerUp application.
5. Set up MySQL database:
   - Run the setup script: `mysql -u <username> -p < setup_mysql_dev.sql`
   - Replace `<username>` with your MySQL username.
   - This will create the necessary database structure for the application.
6. Start the API and Profile services:
   - Copy the service files to the appropriate location: `sudo cp api.service /etc/systemd/system/` and `sudo cp profile.service /etc/systemd/system/`
   - Reload systemd: `sudo systemctl daemon-reload`
   - Start the services: `sudo systemctl start api.service` and `sudo systemctl start profile.service`
   - The API and Profile services will now be running.

Note: Ensure you enable the necessary permissions and access rights to perform these installation steps.

## Usage 🎯
1. Ensure that you have completed the installation steps mentioned above.
2. Open your web browser and visit: `http://localhost`
3. Login with your GitHub account credentials to authenticate yourself.
4. Explore the different sections and features of the PartnerUp application.

## Getting Started 🌠
<img src="assets/login_page.png" alt="PartnerUp Login Page" width="400px">

Using PartnerUp is simple and efficient. After logging in with their GitHub account, users can navigate to the find partner section.

<img src="assets/profile_page.png" alt="PartnerUp Profile Page" width="400px">
<img src="assets/search_page.png" alt="PartnerUp Search Page" width="400px">

Here, they can specify their preferences for project partners, such as commits, or other criteria.

<img src="assets/match_page.png" alt="PartnerUp Match Page" width="400px">

Our application then analyzes coding styles, commits, and repositories to filter potential partners based on the user's preferences. This tailored approach helps students find suitable project partners quickly and easily.

<img src="assets/previous_matches.png" alt="PartnerUp Login Page" width="400px">

Users will also have access to previous matches made by our application.

## Demo 📹
Here is a GIF demonstrating the usage of PartnerUp:

<img src="assets/partnerup_gif.gif" alt="PartnerUp Web Demo" height="300">

## Technologies 🧑‍💻
- **Libraries**
    - Flask: web framework for Python
    - PyGithub: library for interacting with the GitHub API using Python
    - Jinja2: template engine for Flask
    - jQuery: front-end library for CSS and JavaScript
    - SQLAlchemy: high-level tools for working with databases
    - MySQLdb: python interface for connecting to a MySQL database
    - Matplotlib: plotting library for Python
    - Flask-Cors: flask extension for handling cross-origin resource sharing

- **Server Software**
    - Nginx: high-performance web server and reverse proxy server
    - Gunicorn: WSGI HTTP server for Python

- **Languages**
    - Python: backend language for building the web application
    - HTML/CSS: frontend language for building the web application

- **Platforms**
    - GitHub: source code hosting platform
    - AWS EC2 Server: web application hosting platform

- **Frameworks**
    - Flask: web framework for building the web application
    - Bootstrap: frontend framework for making the web application responsive

- **Database**
    - MySQL: open-source relational database management system
 
- **Resources**
    - GitHub API documentation: for accessing GitHub data using the API
    - PyGitHub documentation: for working with GitHub API
    - Flask documentation: for working with the Flask web framework
    - Bootstrap documentation: for working with Bootstrap components

- **Design**
    - Balsamiq: wireframing and prototyping tool
    - Adobe Illustrator: vector graphics editor
    - Adobe Photoshop: raster graphics editor

- **Project Management**
    - Trello: project management and collaboration tool

## APIs and Methods 🔑
- **API Routes**
    - /api/users   
    POST: This route is used to submit the user's GitHub username

    - /api/users/<user_id>  
    GET: This route is used to retrieve information about a specific user  
    DELETE: This route is used to delete a specific user

    - /api/users/<user_id>/partners  
    GET: This route is used to retrieve a specific user’s partners

    - /api/users/<user_id>/partners/<partner_id>  
    GET: This route is used to retrieve a specific user’s partner  
    POST: This route is used to submit a specific user’s partner  
    DELETE: This route is used to delete a specific user’s partner

- **3rd-party API**
    - PyGitHub proved to be a valuable tool for interacting with the GitHub API, eliminating the need for direct interaction with the API itself.

## Future Features 📇
- **Enhanced Partner Matching**: Currently, the application matches users based on commits and other criteria specified in their preferences. 
In the future, additional factors such as project interests, past experience, and availability could be considered to improve the accuracy of partner matching.
This could involve incorporating machine learning algorithms or expanding the range of data analyzed from GitHub profiles.

- **Reputation and Feedback System**: Implementing a reputation and feedback system would enable users to provide feedback on their project partners' collaboration skills and performance.
This would help build a community-driven platform where users can make more informed decisions when selecting partners for future projects.

## Known Bugs 🐛
- **Slow Match Functionality**: The current implementation of the match functionality experiences a delay of approximately 15 seconds or more in finding a match.
This delay is caused by factors such as API response time, processing complexity, and data volume.
Addressing these factors and optimizing the match functionality is a priority for future versions of the application.
The goal is to reduce the processing time and provide users with a faster and more efficient matching experience.

## Contributing 🔼
We welcome contributions from the community. To contribute to PartnerUp, follow these steps:
1. Fork the repository
2. Create your feature branch: `git checkout -b feature`
3. Commit your changes: `git commit -am 'Add my feature'`
4. Push to the branch: `git push origin feature`
5. Submit a pull request

## License 📋
PartnerUp is released under the [MIT License](LICENSE)

## Authors 👨
**Ajisafe Oluwapelumi** - Designer & Software Engineer
- [GitHub](https://github.com/ajipelumi)  
- [LinkedIn](https://www.linkedin.com/in/ajisafeoluwapelumi/)  
- [Twitter](https://twitter.com/the_pelumi)  
- [Dev](https://dev.to/ajipelumi)  

## Acknowledgement 🌟
- ALX Staff & Students  
- Holberton School Staff & Students  
- Abdulqadir Ahmad  
- Olagunju Abraham  
- Durojaiye Oladipupo  
- Durojaiye Dickson  
- You
