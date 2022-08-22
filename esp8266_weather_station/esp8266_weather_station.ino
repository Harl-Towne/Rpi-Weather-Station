#include <ESP8266WiFi.h>
#include "DHT.h"

/* TODO
 *  Fix bouncing? on wind speed and rain sensors (shift register)
 *  fix wind direction sensor reading N between NE and E, and other related issues (CC source)
 *  Implement a reliable method for wind gust measurement (probably need to fix bouncing first)
*/

// networking shit
WiFiServer server(80);
IPAddress IP(192, 168, 4, 15);
IPAddress mask = (255, 255, 255, 0);

// sensor shit
const uint8_t windSpeed_pin = D5;
const uint8_t windDirection_pin = A0;
const uint8_t rain_pin = D7;
const uint8_t DHT_pin = D3;
#define DHTTYPE DHT11
DHT dht(DHT_pin, DHTTYPE);

// measurment details
#define measurment_interval 2000
#define wind_dir_measurment_interval 50
#define history_length (60*5) // seconds of history to store
unsigned long last_measurement = measurment_interval;
unsigned long last_wind_dir_measurement = 0;

// constants
const float wind_increment_dist = 0.109956;
const float rain_increment_vol = 2.136752;  // fix this value
const int wind_direction_vals[] = {20, 33, 64, 212, 711, 511, 363, 120};
const char wind_directions[8][3] = {
                      "S",
                      "SW",
                      "W",
                      "NW",
                      "N",
                      "NE",
                      "E",
                      "SE"};
                   
// other shit
uint8_t last_wind_val = 0;
unsigned long last_wind_time = 0;
uint8_t last_rain_val = 0;
unsigned long last_rain_time = 0;

// counters
unsigned int wind_increments = 0;
unsigned int rain_increments = 0;
unsigned long wind_dir_increments[] = {0, 0, 0, 0, 0, 0, 0, 0};

// history
#define history_epochs (history_length * 1000 / measurment_interval)
uint8_t current_epoch = 0; // current epoch that hasn't yet been saved into history arrays
uint8_t last_unsent_epoch = 0; // oldest epoch that hasn't been sent
float wind_speed_hist[history_epochs];
float rain_hist[history_epochs];
uint8_t wind_dir_hist[history_epochs];
float temp_hist[history_epochs];
float humidity_hist[history_epochs];


void setup()
{
  // start serial
  Serial.begin(115200);
  delay(1000);
  Serial.println("Waiting...");
  delay(4000);

  // setup access point
  Serial.print("Setting soft-AP ... ");
  WiFi.mode(WIFI_AP);
  if(WiFi.softAP("WeatherBaseStation", "password1"))
  {
    Serial.println("Ready");
  }
  else
  {
    Serial.println("Failed!");
  }
  WiFi.softAPConfig(IP, IP, mask);
  server.begin();

  // setup pins
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(windSpeed_pin, INPUT);
  pinMode(windDirection_pin, INPUT);
  pinMode(rain_pin, INPUT);
  dht.begin();

  // initialise variables
  last_wind_val = digitalRead(windSpeed_pin);
  last_measurement = millis();
}


void loop()
{
  //#####################
  // respond to requests
  //#####################
  WiFiClient client = server.available();
  if(client)
  {
    String request = client.readStringUntil('\r');
    Serial.println("********************************");
    Serial.print("From the station: " + request + " at ");
    Serial.print(millis());
    Serial.println("ms");
    if(request == "GET / HTTP/1.1" && last_unsent_epoch != current_epoch)
    {
      bool original_led = digitalRead(LED_BUILTIN);
      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
      Serial.println("valid data request");
      Serial.print("Sending from: ");
      Serial.print(last_unsent_epoch);
      Serial.print("\t(current recording is at: ");
      Serial.print(current_epoch);
      Serial.println(")");
      Serial.println("Epochs sent:");
      
      client.println("HTTP/1.0 200 OK");
      client.println("Feilds: wind_speed, rain, wind_direction, temperature, humidity");
      client.print("MeasurementInterval: ");
      client.println(measurment_interval);
      client.print("StartEpoch: ");
      client.println(mod(last_unsent_epoch-current_epoch,  history_epochs) - history_epochs);
      client.println("");
      for(int i = last_unsent_epoch; i % history_epochs != current_epoch; i++)
      {
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
        Serial.println(i % history_epochs);
        int j = i % history_epochs;
        client.print(wind_speed_hist[j]);
        client.print(", ");
        client.print(rain_hist[j]);  
        client.print(", ");
        client.print(wind_dir_hist[j]);
        client.print(", ");
        client.print(temp_hist[j]);
        client.print(", ");
        client.println(humidity_hist[j]);
      }

      Serial.println("Sample data:");
      Serial.print("Wind-S:\t");
      Serial.println(wind_speed_hist[last_unsent_epoch]);
      Serial.print("Wind-D:\t");
      Serial.println(wind_dir_hist[last_unsent_epoch]);
      Serial.print("Rain:\t");
      Serial.println(rain_hist[last_unsent_epoch]);  
      Serial.print("Temp:\t");
      Serial.println(temp_hist[last_unsent_epoch]);
      Serial.print("Hum:\t");
      Serial.println(humidity_hist[last_unsent_epoch]);

      last_unsent_epoch = current_epoch;
      
      digitalWrite(LED_BUILTIN, original_led);
    }
    else if(last_unsent_epoch != current_epoch)
    {
      Serial.println("valid data request but there is no data");
      client.println("HTTP/1.0 204 No Content");
    }
    else
    {
      Serial.println("invalid data request");      
      client.println("HTTP/1.0 400 Bad Request");
    }
    client.flush();
  }

  //###################################
  // aggregate and record measurements
  //###################################
  if((unsigned long)(millis() - last_measurement) > measurment_interval)
  {
    last_measurement = millis();
//    Serial.printf("Stations connected = %d\n", WiFi.softAPgetStationNum());
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));

    // record wind speed
    float wind_speed = wind_increment_dist * 2 * wind_increments * 1000 / measurment_interval;
    wind_increments = 0;

    // record rain vol
    float rain_vol = rain_increment_vol * rain_increments;
    rain_increments = 0;

    // record wind direction
    uint8_t maxx = 0;
    unsigned int max_val = wind_dir_increments[maxx];
    wind_dir_increments[0] = 0;
    for(int i = 1; i < 8; i++)
    {
      if(wind_dir_increments[i] > max_val)
      {
        maxx = i;
        max_val = wind_dir_increments[i];
      }
      wind_dir_increments[i] = 0;
    }
    uint8_t wind_direction = maxx;

    // record temperature & humidity
    float temp = dht.readTemperature();
    float humidity = dht.readHumidity(); // <======================================================= uncomment 
    // float temp = 25;
    // float humidity = 80;
    Serial.print(temp);
    Serial.print("\t");
    Serial.println(humidity);
    // Check if any reads failed and exit early (to try again).
    if (isnan(temp) || isnan(humidity)) {
      temp = -1;
      humidity = -1;
    }
   
    // save variables to arrays
    wind_speed_hist[current_epoch] = wind_speed;
    rain_hist[current_epoch] = rain_vol;
    wind_dir_hist[current_epoch] = wind_direction;
    temp_hist[current_epoch] = temp;
    humidity_hist[current_epoch] = humidity;
    

    // increment array varibles
    current_epoch++;
    current_epoch = current_epoch % history_epochs;
    if(current_epoch == last_unsent_epoch)
    {
      last_unsent_epoch++;    
      last_unsent_epoch = last_unsent_epoch % history_epochs;
    }
  }

  //####################
  // measure wind speed
  //####################
  if(digitalRead(windSpeed_pin) != last_wind_val)
  {
    if((unsigned long)(millis() - last_wind_time) > 10 && last_wind_val == 1)
    {
      wind_increments++;
    }
    last_wind_val = digitalRead(windSpeed_pin);
    last_wind_time = millis();
  }

  //##############
  // measure rain
  //##############
//  Serial.println(digitalRead(rain_pin));
  if(digitalRead(rain_pin) != last_rain_val)
  {
    if((unsigned long)(millis() - last_rain_time) > 200 && last_rain_val == 0)
    {
      rain_increments++;
    }
    last_rain_val = digitalRead(rain_pin);
    last_rain_time = millis();
  }

  //#########################
  // measure wind direcction
  //#########################
  if((unsigned long)(millis() - last_wind_dir_measurement) > wind_dir_measurment_interval)
  {
    last_wind_dir_measurement = millis();
    int volt = analogRead(A0);
    uint8_t closest = 0;
    int closest_val = abs(volt-wind_direction_vals[closest]);
    for(int i = 1; i < 8; i++)
    {
      if(abs(volt-wind_direction_vals[i]) < closest_val)
      {
        closest = i;
        closest_val = abs(volt-wind_direction_vals[i]);
      }
    }
    wind_dir_increments[closest]++;
  }
}

// modulus function because % is fucked
int mod(int a, int b)
{
    int r = a % b;
    return r < 0 ? r + b : r;
}
