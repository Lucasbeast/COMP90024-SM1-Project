# Data Presentation

## Introduction

### Scenario 1: Exploring the Influence of Weather on Pollen Counts
This study examines the correlation between weather conditions and pollen counts by analyzing weather data and pollen concentration levels.

### Scenario 2: Impact of Air Pollution on Residents' Mood
This section investigates the relationship between air pollution levels and residents' mood by visualizing air quality data alongside sentiment analysis of social media posts.

### Scenario 3: Hot Topics and Sentiments on Social Networks
This section visualizes and analyzes the trending topics on social networks over a specific time period using word clouds.

## Installation

To get started, you need to install the required dependencies. Follow these steps:

1. **Clone the repository:**
   ```sh
   git clone <your-repository-url>
   cd <your-repository-directory>

2. **Create a virtual environment (optional, but recommended):**
   ```python -m venv env
      source env/bin/activate # For macOS and Linux  
      .\env\Scripts\activate  # For Windows
   ```

3. **Install required packages:**
    pip install -r requirements.txt

## Usage

### Running Jupyter Notebook and Dash Applications

This project uses Jupyter Notebook for data analysis and visualization, with embedded Dash applications. Follow these steps to run the Jupyter Notebooks:

1. **Start Jupyter Notebook:**

    ```sh
    jupyter notebook
    ```

2. **Open Notebooks:**

    In your web browser, open the URL provided in the terminal (usually something like `http://127.0.0.1:8888` or a similar port number). Navigate to the `frontend` folder and open the corresponding `.ipynb` files:

    - `scenario1.ipynb`: Contains the analysis and visualization of the relationship between weather and pollen counts, along with a Dash application.
    - `scenario2.ipynb`: Contains the analysis and visualization of the relationship between air pollution and residents' mood, along with two Dash applications.
    - `scenario3.ipynb`: Contains the analysis and visualization of trending topics and sentiments on social networks.

3. **Run Dash Applications:**

    - **For `scenario1.ipynb`:**
      - Run the code cells to start the Dash application.
      - After starting the Dash server, the application can be accessed at [http://127.0.0.1:8050](http://127.0.0.1:8050).
      - An embedded IFrame will display the Dash application within the notebook.

    - **For `scenario2.ipynb`:**
      - Run the code cells to start the first Dash application.
      - After starting the Dash server, the first application can be accessed at [http://127.0.0.1:8051](http://127.0.0.1:8051).
      - An embedded IFrame will display the first Dash application within the notebook.
      - Run the code cells to start the second Dash application.
      - After starting the second Dash server, the second application can be accessed at [http://127.0.0.1:8052](http://127.0.0.1:8052).
      - An embedded IFrame will display the second Dash application within the notebook.

## Project Structure

Ensure your project has the following structure:
frontend/
├── .ipynb_checkpoints/
├── image/
├── README.md
├── requirements.txt
├── scenario1.ipynb
├── scenario2.ipynb
├── scenario3.ipynb


## Data

### Data Sources

- **Weather Data:** Collected historical weather data for the Melbourne region.
- **Pollen Data:** Includes pollen data from 2016 to 2020.
- **Air Quality Data:** Includes EPA air quality data for a specific date range.
- **Twitter Sentiment Data:** Twitter sentiment analysis data used to study the impact of air pollution on residents' mood.

### Data Files

Data files are included in the `data` directory of the project and are processed in detail in each scenario's Notebook.

## Scenarios

### Scenario 1: Weather and Pollen Counts

Refer to `scenario1.ipynb` for detailed analysis and visualization, including an embedded Dash application.

### Scenario 2: Air Pollution and Mood

Refer to `scenario2.ipynb` for detailed analysis and visualization, including two embedded Dash applications.

### Scenario 3: Hot Topics and Sentiments

Refer to `scenario3.ipynb` for detailed analysis and visualization.

## Contributing

Contributions are welcome! Please submit pull requests or report issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

