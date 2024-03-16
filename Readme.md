# Weather Visualisation using matplotlib library

This project is inspired by a tutorial I saw on [finxter.com](https://blog.finxter.com/how-i-visualized-daily-temperature-over-50-years-in-your-home-town/) where the author created a visualization of the temperatures for the past 50 years in the US and north pole.

The `main.py` file makes an api call to [archive-api.open-meteo.com](https://open-meteo.com/en/docs/historical-weather-api), processes the response and saves the information into a json file.

The `variables.py` contains variables that are reused in this project.

The other files are different methods of visualizing the data. Each file creates a plot and saves it locally:
* `50years_one_day.py` creates a scatter plot that shows the difference in temperatures on the 1st day of each month for the past 53 years.
* `animated_50years_monthly.py` Creates an animated scatter plot that shows the temperatures on the same day for each month for the past 53 years.
* `annotated_with_lines.py` Creates an annotated plot with a vertical and horizontal lines highlighting the lowest temperature in the selected date range.
* `plotting_dubai.py` In this file I am applying many plotting concepts and created a figure with multiple subplots: line chart, pie chart, histogram, plot with 2 axes.

# To run the project
1. Make sure you have at least python 3.5 installed
2. Create a virtual environment and install requirements:

   * For Windows 
    ```
    py -m venv .env
    .env\Scripts\activate.bat
    pip install -r requirements.txt
    ```
    * For Unix 
    ```
    python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt
    ```
3. Run the desired python file using: `python3 [filename.py]`

