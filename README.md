# Toohla
Add PATH for chromedriver and Chrome app as per you local machine
import carbon emission file from PATH on your local machine
for testing purpose I have set the car to "taxi".

#My API development approach

The API call should be in this format http://localhost:5000/walk?origin={origin}s&destination={destination}

In order to implement this API solution, I broke the whole implication process into 3 segments. As we are dealing with 3 different sources of details and 3 different outputs.

In the first segment I decided to implement the solution for “Car” distance, time and CO2 emission. 
First we need to get the correct data from the Google API, as using the Google Developer Maps API is a costly method. We need to consider some other solution to implement this segment. 
Directly using the google maps url is a general way, but after further research there are many API, JS, CSS scripts which are running in background which gives us our actual geolocation result. 
To make the queries dynamic, I used the furl library to create segments and arguments for the host url, after I got the values(origin and destination) inserted by the user, I passed them to Google Maps url. To get the car make and model, I used the same concept as I used for origin and destination.
To get the final page result we need to use Selenium to make the request, which means masking it directly like a request as a browser would make and store the html content after the request is completed. So, I did that.
After getting the correct and whole html content, I converted the content into a lxml etree so that to get any values and any id we can directly create a dynamic “Xpath”.
TO calculate the carbon emission, importing the csv file for car make and model then running a pandas query to find the car CO2 stats which the user is looking for and adding it to the result json.
After configuring Xpath for all the result values, in our case Distance, Time and Carbon emission. We can directly return the json response.

To further optimize this solution instead of using a single selenium webdriver instance every time  we can create a selenium grid and  host it on any cloud computing platform like AWS and use that to make this system an automation tool. It will reduce our latency furthermore. Also storing the html content on database would make this system more efficient because then we can divide the code into 2 parts, one service to use selenium and get the html content and save it to database and second service to do all the scraping and calculations and other processes which doesn’t require selenium session or much computing power.





#Train solution Approach

As seen on the provided dataset from https://data.cityofchicago.org/Transportation/CTA-System-Information-List-of-L-Stops/8pix-ypme we can see the coordinates of every train station in the Chicago area.
To find the shortest possible path with least carbon emission. We need to create a node of each train station with their respective color lines.
If our origin is a station where its coordinates are (x,y) and it lies on the pink line and our destination is at coordinates (p,q) and it lies on the blue line. Then we need to keep traveling on the pink line station until we encounter a station which shares lines with blue.
Then we travel the link until we reach our destination.
We also keep the direction attribute in check as well, because it will determine if there are multiple possible nodes(stations to go) which one is aligning with the direction of train traffic.
We can use Dijkstra’s Shortest Path Algorithm to find out the best possible path for our journey. 

Reference: https://i0.wp.com/transitmap.net/wp-content/uploads/2013/09/tumblr_msq35v5WEM1r54c4oo4_1280.jpg?resize=1194%2C1535&ssl=1

