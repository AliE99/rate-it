# Rate It

The **Rate It** is a Django Application where users can create and view posts and rate them.


## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)


## Project Overview

This Django application, built using Django Rest Framework (DRF), allows users to view a list of posts and submit ratings. Each post contains a title and text, and users can rate the posts on a scale of 0 to 5. The rating system ensures that each user's rating can be updated if they rate a post again.

### Features

- **Post List View:** Displays the title of each post, the number of users who have rated it, and the average rating. If a user has rated a post, their rating is shown as well.
- **Submit Rating:** Users can submit a rating for a post, and their rating is updated if they rate the post again. There is no functionality to delete a rating.
- **Performance at Scale:** The application is designed to handle a large number of ratings per post (potentially millions), ensuring it performs well under high traffic, capable of handling thousands of requests per second.
- **Rating Stability:** To prevent short-term events like organized campaigns or emotional ratings from affecting the post's average score, a mechanism has been implemented to stabilize the rating system against unrealistic spikes.

This project focuses on providing an efficient and scalable solution for displaying and rating posts, ensuring reliability even under heavy load and high traffic.