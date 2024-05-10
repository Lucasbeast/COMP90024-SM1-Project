const fs = require('fs');
const https = require('https');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// Helper function to read configuration values
function readConfig(key) {
  try {
    return fs.readFileSync(`/etc/myapp/configs/default/shared-data/${key}`, 'utf8').trim();
  } catch (err) {
    console.error(`Error reading config ${key}:`, err);
    process.exit(1); // Exit if configuration cannot be loaded
  }
}

const username = readConfig('ES_USERNAME');
const password = readConfig('ES_PASSWORD');

const pollenData = require('./canberra_act.json');

const options = {
  hostname: 'localhost',
  port: 9200,
  path: '/pollen/_doc?routing=canberra',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  auth: `${username}:${password}`
};

// Function to add days to a given date string in the format 'yyyy-MM-dd'
function addDays(dateStr, days) {
  const date = new Date(dateStr);
  date.setDate(date.getDate() + days);
  return date.toISOString().split('T')[0]; // Return only the date part in 'yyyy-MM-dd' format
}

function sendDataToElastic(body) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let responseData = '';
      console.log(`statusCode: ${res.statusCode}`);
      
      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        console.log('Response from Elasticsearch:', responseData);
        resolve(responseData);
      });
    });

    req.on('error', (error) => {
      console.error('Error sending data to Elasticsearch:', error);
      reject(error);
    });

    req.write(JSON.stringify(body));
    req.end();
  });
}

async function insertData() {
  for (const feature of pollenData.features) {
    const startDate = feature.properties.start_date.split('T')[0];
    const endDate = addDays(startDate, 7); // Adding 7 days

    const body = {
      id: feature.id,
      area: 'canberra', // Assuming 'area' is a constant
      poaceae_pollen: feature.properties.poaceae_pollen_concentration_grains_metre_cubed || 0,
      other_pollen: feature.properties.other_pollen_concentration_grains_metre_cubed || 0,
      longitude: feature.geometry.coordinates[0],
      latitude: feature.geometry.coordinates[1],
      start_date: startDate,
      end_date: endDate,
    };

    try {
      await sendDataToElastic(body);
    } catch (error) {
      console.error('Failed to insert data:', error);
    }
  }
}

insertData();
