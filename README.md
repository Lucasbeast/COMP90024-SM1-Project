## Introduction
This project develops a data analysis system using Twitter, climate, and environmental data on the Melbourne Research Cloud. Our system analyzes air pollution and predicts residents' mental health by combining real-time environmental data with historical Twitter data. The interactive front-end allows users to access important information through intuitive graphical representations, reducing the complexity and cost of analysis.

## System Overview
The system leverages cloud technologies like Kubernetes, Fission, and Elasticsearch to handle large-scale data management. It integrates datasets from SUDO, Twitter, EPA, and BoM to perform analyses and visualizations. Key components include:
- **Data ingestion pipeline:** Streams data processing and storage in Elasticsearch.
- **Local uploads:** Stores static data in Elasticsearch.
- **Jupyter Notebook front-end:** Provides an interactive and user-friendly interface.

## Objectives
- Analyze the impact of weather on pollen concentration.
- Study the effect of air pollution on public mood.
- Analyze Twitter sentiment of Melbourne residents.

## Scenario Descriptions

### Scenario 1: Weather and Pollen Concentration
Analyzes the influence of weather on pollen levels. By combining predicted pollen data with recent weather data, we visualize trends and correlations using tools like time series plots, scatter plots, and bubble plots. This helps understand the impact of weather factors on pollen concentrations.

### Scenario 2: Air Pollution and Public Mood
Studies the impact of air pollution (PM2.5) on public sentiment using Twitter data. An interactive map, time series, scatter plots, bar charts, box plots, and heatmaps are used to explore the relationship between air pollution and public mood. This helps formulate health recommendations related to air pollution.

### Scenario 3: Twitter Sentiment Analysis
Generates word clouds to visualize trending topics and public sentiment on Twitter. This scenario can be combined with the previous two to monitor emotional dynamics during high pollen counts or high air pollution periods.

## Directory Structure
- **.git/**: Version control history and configuration.
- **.idea/**: IDE-specific settings.
- **backend/**: Backend code and related files.
- **data/**: Datasets and data files.
- **database/**: Database schemas and migrations.
- **docs/**: Project documentation.
- **frontend/**: Frontend code and related files.
- **test/**: Test cases and scripts.
