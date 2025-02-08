# ShellYeah! Fantasy Basketball

## Overview  
ShellYeah! Fantasy Basketball is a web application designed to enhance the fantasy basketball experience for leagues hosted on [Sleeper](https://sleeper.com/). While Sleeper provides a robust fantasy sports platform, its fantasy basketball support is somewhat limited.  

This project aims to **fill in the gaps** by providing additional tools to assist in league management—starting with a **draft lottery simulation** and expanding toward more advanced features like **in-depth player stats, trade analyzers, and more**.  

## Features  
✔️ **Player List** – Displays all NBA players currently tracked by Sleeper.  
✔️ **League Selection & Draft Lottery** – Users can enter their **Sleeper username**, retrieve their leagues, and simulate a draft lottery based on the previous season’s standings.  
✔️ **Odds Customization** – The draft lottery odds can be manually adjusted, provided they sum to 100%.  
✔️ **Automated API Integration** – The app interacts with **Sleeper’s API** to fetch real-time fantasy league data.  

## How It Works  
1. **Navigate to the Lottery Simulation Tool**  
   - Click the **"Lottery Sim"** option under the **"Projects"** dropdown in the navbar.  

2. **Enter Your Sleeper Username**  
   - The backend fetches your unique **user_id** via Sleeper’s API.  

3. **Select Your League**  
   - A list of all your **active NBA fantasy leagues** is displayed.  
   - Choose one to proceed.  

4. **Generate Draft Lottery Odds**  
   - The backend retrieves **last season’s league data** to determine team records.  
   - These records **automatically set the draft lottery odds**, but you can modify them as long as they total 100%.  

5. **Run the Lottery Simulation**  
   - Click **"Submit"** to simulate the draft lottery and determine the draft order for bottom teams.  


![ShellYeahDemo-ezgif com-speed](https://github.com/user-attachments/assets/c83270dc-c974-4790-ba31-96b53c56790e)


## Tech Stack  
- **Django 4.2.13** (Web Framework)  
- **Python 3.10.12**  
- **whitenoise 6.6.0** (Serving static files)  
- **Sleeper API** (Fantasy league data source)  
- **Requests Library** (Handling API interactions)  

## Data Handling  
- **League Data Source** – All league data is fetched from **Sleeper’s API** via a custom-built Python script using the `requests` library.  
- **Local Database Storage** – Once retrieved, league data is stored **locally** to allow for additional calculations and insights without repeatedly querying Sleeper’s API.  

## Installation & Setup  
1. Clone the repository:  
   ```sh
   git clone https://github.com/yourusername/shellyeah-fantasy-basketball.git
   cd shellyeah-fantasy-basketball
2. Install dependencies:
   ```sh
    pip install -r requirements.txt
3. Run the Django development server:
   ```sh
   python manage.py runserver
4. Access the web app at:
   http://127.0.0.1:8000/

## Future Plans 🚀
- **Advanced Player Stats for better decision-making
- **Trade Analyzer to assess trade fairness and impact
- **Matchup Projections based on historical team performance
- **Deployment to make the tool publicly accessible

## Who Is This For?
This project is designed for fantasy basketball managers using Sleeper who want more control and insights into their leagues. It also serves as a showcase of my backend development skills, particularly in API integration, database management, and Django web development.
