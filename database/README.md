# Database Setup

This project contains scripts for setting up and managing various Elasticsearch indices and data imports for different datasets. The following directories and their contents are part of this project:

## Directory Structure

- **database**
  - **bom**
    - `createIndexBom.sh`: Shell script to create an Elasticsearch index for BOM data.
    - `setupBomLifecyclePolicy.sh`: Shell script to set up the lifecycle policy for BOM data in Elasticsearch.
  - **epa**
    - `createIndexEpa.sh`: Shell script to create an Elasticsearch index for EPA data.
    - `setupEpaLifecyclePolicy.sh`: Shell script to set up the lifecycle policy for EPA data in Elasticsearch.
  - **pollen**
    - `createIndexPollen.sh`: Shell script to create an Elasticsearch index for Pollen data.
    - `loadPollenCampbelltown.js`: JavaScript file to load Pollen data for Campbelltown.
    - `loadPollenCanberra.js`: JavaScript file to load Pollen data for Canberra.
    - `loadPollenParkville.js`: JavaScript file to load Pollen data for Parkville.
    - `loadPollenRocklea.js`: JavaScript file to load Pollen data for Rocklea.
  - **sensor**
    - `createIndexSensor.sh`: Shell script to create an Elasticsearch index for Sensor data.
    - `loadSensor.js`: JavaScript file to load Sensor data.
  - **twitter**
    - `twitterIndex.py`: Python script to create an Elasticsearch index for Twitter data.
    - `twitterToElastic.py`: Python script to import Twitter data into Elasticsearch.
    - `twbxtIndex.py`: Python script to create an Elasticsearch index for Twitter BXT data.
    - `twbxtToElastic.py`: Python script to import Twitter BXT data into Elasticsearch.


- **docs**
    - `elastic.env`: Environment variables file for Python scripts.
    - `ES_USERNAME`: File containing the Elasticsearch username.
    - `ES_PASSWORD`: File containing the Elasticsearch password.


## Installation

To get started, you need to install the required dependencies. Follow these steps:


1. **Clone the repository:**
  ```sh
   git clone <your-repository-url>
   cd <your-repository-directory>

2. **Create a virtual environment (optional, but recommended):**
  ```
   python -m venv env
   source env/bin/activate # For macOS and Linux  
   .\env\Scripts\activate  # For Windows
   ```

3. **Install required packages:**
   pip install -r requirements.txt

## Scripts

### BOM Scripts
- **createIndexBom.sh**: 
  - Purpose: Creates an Elasticsearch index for BOM data.
  - Usage: `./createIndexBom.sh`


- **setupBomLifecyclePolicy.sh**: 
  - Purpose: Sets up the lifecycle policy for BOM data in Elasticsearch.
  - Usage: `./setupBomLifecyclePolicy.sh`
  
- Note: Ensure `ES_USERNAME` and `ES_PASSWORD` environment variables are set before execution. Use `chmod 600` to secure these files.

### EPA Scripts
- **createIndexEpa.sh**: 
  - Purpose: Creates an Elasticsearch index for EPA data.
  - Usage: `./createIndexEpa.sh`

  
- **setupEpaLifecyclePolicy.sh**: 
  - Purpose: Sets up the lifecycle policy for EPA data in Elasticsearch.
  - Usage: `./setupEpaLifecyclePolicy.sh`
  
- Note: Ensure `ES_USERNAME` and `ES_PASSWORD` environment variables are set before execution. Use `chmod 600` to secure these files.

### Pollen Scripts
- **createIndexPollen.sh**: 
  - Purpose: Creates an Elasticsearch index for Pollen data.
  - Usage: `./createIndexPollen.sh`

  
- **loadPollenCampbelltown.js**: 
  - Purpose: Loads Pollen data for Campbelltown into Elasticsearch.
  - Usage: `node loadPollenCampbelltown.js`
  
  
- **loadPollenCanberra.js**: 
  - Purpose: Loads Pollen data for Canberra into Elasticsearch.
  - Usage: `node loadPollenCanberra.js`
  
  
- **loadPollenParkville.js**: 
  - Purpose: Loads Pollen data for Parkville into Elasticsearch.
  - Usage: `node loadPollenParkville.js`
  
  
- **loadPollenRocklea.js**: 
  - Purpose: Loads Pollen data for Rocklea into Elasticsearch.
  - Usage: `node loadPollenRocklea.js`
  

### Sensor Scripts
- **createIndexSensor.sh**: 
  - Purpose: Creates an Elasticsearch index for Sensor data.
  - Usage: `./createIndexSensor.sh`
  
  
- **loadSensor.js**: 
  - Purpose: Loads Sensor data into Elasticsearch.
  - Usage: `node loadSensor.js`
  
- Note: Ensure `ES_USERNAME` and `ES_PASSWORD` environment variables are set before execution. Use `chmod 600` to secure these files.

### Twitter Scripts
- **twitterIndex.py**: 
  - Purpose: Creates an Elasticsearch index for Twitter data.
  - Usage: `python twitterIndex.py`
  
  
- **twitterToElastic.py**: 
  - Purpose: Imports Twitter data into Elasticsearch.
  - Usage: `python twitterToElastic.py`
  
  
- **twbxtIndex.py**: 
  - Purpose: Creates an Elasticsearch index for Twitter BXT data.
  - Usage: `python twbxtIndex.py`
  
  
- **twbxtToElastic.py**: 
  - Purpose: Imports Twitter BXT data into Elasticsearch.
  - Usage: `python twbxtToElastic.py`
  
- Note: Ensure `elastic.env` is in the same directory as the script.

## Setup Instructions

1. **Credential Files**:
   - Store your Elasticsearch credentials in `docs/ES_USERNAME` and `docs/ES_PASSWORD` files.
   - Ensure the permissions for these files are set to read-only for the owner: `chmod 600 ES_USERNAME ES_PASSWORD`.

2. **Environment Variables**:
   - For Shell and JavaScript scripts, set the `ES_USERNAME` and `ES_PASSWORD` environment variables from the credential files.
   - Example:
     ```bash
     export ES_USERNAME=$(cat /path/to/docs/ES_USERNAME)
     export ES_PASSWORD=$(cat /path/to/docs/ES_PASSWORD)
     ```

3. **Python Environment**:
   - Ensure the `elastic.env` file is placed in the same directory as the Python scripts.

4. **Running Scripts**:
   - Ensure Elasticsearch is running and accessible at the configured endpoint before executing any scripts.
   - Set the execution permission for Shell scripts with:`chmod +x <script_name>.sh`
   - Follow the usage instructions provided for each script in the respective sections above.


