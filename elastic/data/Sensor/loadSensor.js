const fs = require('fs');
const https = require('https');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// Helper function to read configuration values
function readConfig(key) {
  try {
    // 
    return fs.readFileSync(`/etc/myapp/configs/default/shared-data/${key}`, 'utf8').trim();
  } catch (err) {
    console.error(`Error reading config ${key}:`, err);
    process.exit(1); // Exit if configuration cannot be loaded
  }
}

const username = readConfig('ES_USERNAME');
const password = readConfig('ES_PASSWORD');

const sensorData = require('./meshed-sensor-type.json');

const options = {
  hostname: 'localhost',
  port: 9200,
  path: '/sensor/_doc?routing=sensor',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  auth: `${username}:${password}`
};

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
  for (const data of sensorData) {
    const [date, time] = data.time.split('T');
    const body = {
      date: date,
      time: time.replace('+00:00', ''),
      dev_id: data.dev_id,
      temperature: data.temperature,
      humidity: data.humidity,
      battery: data.battery,
      location: {
        lat: data.lat_long.lat,
        lon: data.lat_long.lon
      }
    };

    try {
      await sendDataToElastic(body);
    } catch (error) {
      console.error('Failed to insert data:', error);
    }
  }
}

insertData();
