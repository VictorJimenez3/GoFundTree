# GoFundTree: AR-Driven Urban Greening Platform

## Short Description
GoFundTree is a mobile-first Augmented Reality (AR) web application that empowers users to visualize urban reforestation projects by placing virtual trees in their environment. By combining AR visualization with real-world donation capabilities, GoFundTree helps raise awareness for green initiatives and funds tree-planting efforts in urban spaces. Designed for accessibility, engagement, and sustainability.

## Features
- **Augmented Reality Tree Placement**: Visualize how urban spaces would look with added greenery.
- **Donation Integration**: Connects users to real-world tree-planting initiatives directly from the app.
- **Cross-Platform Mobile Web App**: Accessible on iOS and Android without the need for native app installation.
- **Photo Sharing**: Snap and share AR visualizations to promote environmental awareness.
- **Cloud-Based Data Management**: Efficiently manages AR models, user images, and donation records.

## Tech Stack
- **AR Frontend**: ModelViewer (web-based AR library), Blender (tree model creation), HTML5, CSS3, JavaScript.
- **Backend**: Python, Flask, Jinja templates.
- **Database and Storage**: Google Cloud Platform (GCP), Firebase Storage.
- **Deployment**: Docker for containerized backend deployment, GitHub for version control.

## Challenges and Solutions
- **3D Model Optimization**: Balanced visual fidelity and performance to ensure smooth AR experiences on mobile.
- **Cross-Device Compatibility**: Rigorous testing and adjustments to ensure consistent AR functionality across different smartphones and browsers.
- **Seamless Backend Integration**: Designed and implemented APIs to handle image uploads, model retrieval, and donation transactions efficiently.
- **Performance Optimization**: Reduced AR load times through caching strategies, model compression, and database query tuning.
- **User Experience Design**: Crafted an intuitive, mobile-friendly interface to simplify AR interactions and donation processes.

## Key Outcomes / Metrics
- **Fully Functional MVP**: Delivered a working AR platform supporting virtual visualization and real-world action.
- **Cross-Platform Support**: Achieved device-agnostic AR functionality across Android and iOS.
- **Scalable Cloud Infrastructure**: Deployed an extensible backend ready for future growth and feature expansion.

## How to Run It
Because GoFundTree is an integrated web application, setup involves backend deployment and frontend access:

1. Clone the repository:

       git clone https://github.com/VictorJimenez3/GoFundTree.git
       cd GoFundTree

2. Install dependencies:

       pip install -r requirements.txt

3. Run the backend server locally (or deploy via Docker):

       python app.py

4. Open the web app via a mobile browser to interact with the AR features.

*Note: Some AR functionalities may require HTTPS and mobile device camera permissions for full functionality.*

## Links
- [GitHub Repository](https://github.com/VictorJimenez3/GoFundTree)
- [Devpost Project Page](https://devpost.com/software/gofundtree)
