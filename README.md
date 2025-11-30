# AI Weather Genie

## Overview
AI Weather Genie is a web application that provides weather forecasts using the Open-Meteo API. Users can search for cities or enter latitude and longitude coordinates to retrieve weather data, including temperature, humidity, wind speed, and flood risk. The application features an interactive map for location selection and visualizes weather data through charts.

## Project Structure
```
ai-weather-genie
├── src
│   ├── index.html          # Main HTML structure for the application
│   ├── css
│   │   └── styles.css      # CSS styles for the application
│   ├── js
│   │   ├── main.js         # App bootstrap and event wiring
│   │   ├── map.js          # Leaflet map initialization and marker handling
│   │   ├── geocoding.js    # City search and geocoding logic
│   │   ├── forecast.js      # Fetching and processing weather forecasts
│   │   ├── flood.js        # Fetching flood and river discharge data
│   │   ├── ui.js           # DOM updates and insight generation
│   │   └── chart.js        # Chart.js rendering wrapper
│   └── lib
│       └── vendors.md      # Notes about external CDN libraries used
├── package.json            # npm configuration file
├── .gitignore              # Files and directories to ignore by Git
└── README.md               # Project documentation
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd ai-weather-genie
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Open the application:**
   Open `src/index.html` in your web browser to view the application.

## Usage
- Enter a city name in the search bar to find its weather forecast.
- Alternatively, input latitude and longitude coordinates directly.
- Click on the map to set the location for weather data.
- Select a weather model from the dropdown menu to customize the forecast.
- Click the "Get Forecast" button to retrieve and display the weather information.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.