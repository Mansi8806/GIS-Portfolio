# Post Wildfire Drone Flight Survey Plan 

# Brief Description of Project

# Purpose: Sending drones to capture imagery after fires can help first responders organize their response. 
#   This post-fire management benefits from quick and efficient image collection. 
#   This application allows users to get their drones into the field more quickly by streamlining the planning process. 
#   The user can input known information about their drone's specifications and the area they will be visualizing and can quickly receive data that will help them plan the optimal flight path. 
#   This ensures that the amount of time needed to complete the imaging is minimized, thereby conserving the drone's battery life. 
#   Decreasing the time the drone needs to spend in the air also reduces the potential for flight path conflicts with other air operations. 
#   Determining the minimum number of images required helps ensure the drone does not run out of memory and makes the subsequent image processing more efficient. 
#   Finally, providing the user with an estimate of the price of the survey will simplify budgeting decisions. 

# Inputs: 1. Focal Length of drone camera (mm), ± 0.001 mm  
#   2. Drone Camera Sensor Length (mm), ± 0.001 mm  
#   3. Drone Cameras Sensor Width (mm), ± 0.001 mm  
#   4. Desired right-left overlap between images (%)  
#   5. Desired front-back overlap between images (%)  
#   6. Number of surveys   
#   7. Survey Area Width (km/ mi), ± 0.2mm (if using electronic devices like total station)  
#   8. Survey Area Length (km/ mi), ± 0.2mm  
#   9. Enter Drone Altitude above ground (m/ ft), ± 0.5 m or ± 1.6 ft 

# Outputs: The four outputs below will be displayed to the user in a table.  
#   1. Aerial Footprint Size, ± 1.1 cm  
#   2. Number of Flight Lines   
#   3. Total Number of Images   
#   4. Price of Drone Survey ($/(mi^2) or $/(km^2))

try:
    # Function definition used to calculate the photo size
    def aerialphotosize(altitude, focal_length, x_sensor_length, y_sensor_length):
        """Calculates the photo size"""
        aerialphotosize = (((float(altitude)*1000)/float(focal_length))* float(x_sensor_length)) * (((float(altitude)*1000)/float(focal_length))* float(y_sensor_length))
        aerialphotosize = aerialphotosize / 1000000   # converting from mm^2 to m^2
        return round(aerialphotosize, 2) 

    # Function definition used to calculate the number of flight lines required
    def numflightlines(altitude, focal_length, y_sensor_length, sideoverlap, survey_area_width):
        """Calculates the number of flight lines required for the drone to complete a survey of the entire area"""
        # Equation to calculate the amount of space required between each corresponding flight line
        flight_line_spacing = ((float(altitude)*1000)/float(focal_length)* float(y_sensor_length)) * ((100 - float(sideoverlap)) / 100) / 1000 # Dividing by 1000 to get meters 
        # Equation used to calculate the total number of flight lines required within the area
        flight_lines = round(((float(survey_area_width)*1000) / flight_line_spacing) + 1 ,0)
        return flight_lines

    # Function definition used to calculate the flight line spacing
    def flightlinespacing(altitude, focal_length, y_sensor_length, sideoverlap):
        """Calculates the number of flight lines required for the drone to complete a survey of the entire area"""
        # Equation to calculate the amount of space required between each corresponding flight line
        flight_line_spacing = ((float(altitude)*1000)/float(focal_length)* float(y_sensor_length)) * ((100 - float(sideoverlap)) / 100) / 1000 # Dividing by 1000 to get meters 
        return flight_line_spacing

    # Function definition used to calculate the number of images required to image the entire survey area
    def numimages(altitude, focal_length, x_sensor_length, frontoverlap, survey_area_length, numflightlines):
        """Calculates the number of images required to image the entire survey area"""
        #calculate distance between images (size of images in x-dimension), divide 1000 to convert units to m
        dist_bw_img = ((float(altitude)*1000)/float(focal_length) * float(x_sensor_length)) * ((100 - float(frontoverlap))/100) / 1000 
        #calculate number of images per flight line
        img_per_line = ((float(survey_area_length)*1000) / float(dist_bw_img)) + 1
        #calculate total number of images for survey area
        total_images = round(img_per_line * float(numflightlines),0)
        return total_images

    # Function definition used to calculate the total cost of the survey
    def totalcost(NumImages, PriceperImage):
        """Calculates the total cost per image of the drone survey"""
        cost = round((float(NumImages) * float(PriceperImage)),2)
        return cost

    # Function definition used to plot our drone flight using the turtle module
    def plotflight(NumLines, Length_km, Width_km, NW_Lat, NW_Long):
        """Plots the flight path of the drone using the turtle module"""  

        #convert length from km to m
        Length_m = int(Length_km)*1000
        Width_m = int(Width_km)*1000

        #convert all plotting variables to pixel length (1px = 10m)
        Length_px = Length_m/10
        Width_px = Width_m/10
        Spacing_px = Width_px/NumLines

        #determine size of survey area drawing
        screensize_x = Length_px + 20
        screensize_y = Width_px + 20
        origin_x = (-screensize_x/2) + 10
        origin_y = (screensize_y/2) - 10

        # plot out to the screen using Turtle, set turtles for drone and survey area
        import turtle
        wn = turtle.Screen()
        wn.bgcolor("light gray")
        turtle.screensize(screensize_x,screensize_y)
        turtle.title("Drone Flight")

        survey_area = turtle.Turtle()
        survey_area.pensize(2)
        survey_area.speed(0)

        drone = turtle.Turtle()
        drone.pensize(5)
        drone.color("blue")
        drone.speed(0)

        #draw survey area
        survey_area.up()
        survey_area.goto (origin_x, origin_y)
        survey_area.down()
        for i in range (2):
            survey_area.forward(Length_px)
            survey_area.right(90)
            survey_area.forward(Width_px)
            survey_area.right(90)
        survey_area.right(90)
        survey_area.up()
        survey_area.forward(-3)
        survey_area.stamp()
        survey_area.goto (origin_x-56, origin_y + 13)

        #write NW coordinates and draw compass
        survey_area.write("("+ str(NW_Lat) + ", " + str(NW_Long) + ")")
        survey_area.hideturtle()

        headings = [0, 90, 180, 270]
        compass_origin_x = origin_x - 41
        compass_origin_y = origin_y - 37
        survey_area.up()
        for index in range (4):
            survey_area.goto(compass_origin_x, compass_origin_y)
            survey_area.setheading(headings[index])
            survey_area.forward(15)
            survey_area.stamp()
        survey_area.goto(0,0)

        survey_area.goto(compass_origin_x + 20,compass_origin_y-7)
        survey_area.write("E")
        survey_area.goto(compass_origin_x-2, compass_origin_y+ 17)
        survey_area.write("N")
        survey_area.goto(compass_origin_x-28, compass_origin_y-7)
        survey_area.write("W")
        survey_area.goto(compass_origin_x-2, compass_origin_y-31)
        survey_area.write("S")

        survey_area.hideturtle()



        # assume the drone will always fly in an east-west direction
        CycleLength = int(float(NumLines))+1
        drone.up()
        drone.goto(origin_x, origin_y)
        drone.down()
        for len in range(CycleLength):
            drone.forward(float(Length_px))
            drone.up()
            xpos = drone.xcor()
            ypos = drone.ycor()
            drone.goto(xpos,ypos-Spacing_px)
            drone.right(180)
            drone.down()
        wn.exitonclick()

    def main():
        print ("Post Wildfire Drone Survey Plan")
        print("****************************************************************************************************************")
        print("This program will calculate Aerial Footprint Size, Number of Flight Lines, Total Number of Images,")
        print("and the Total Price of the optimal flight survey path for a drone to collect post wildfire data.")
        print("This programmed is designed for use in Canada using metric measurements")
        print()
        # Assumptions and legal notes
        print("This program assumes that the survey terrain is flat, the drone's altitude does not change within")
        print("a survey, weather conditions support ideal drone flight, and drone operators have all licenses and")
        print("permits required.")
        print()
        print("This program is not responsible for drone sustain damages during a survey and serves only to")
        print("provide specifications for potential survey options.")
        print("****************************************************************************************************************")

        ################################## Start of Inputs ###################################
        # Empty lists for all of our inputs
        altitudes = []
        focal_lengths = []
        x_sensor_lengths = []
        y_sensor_lengths = []
        survey_area_width = []
        survey_area_length = []
        side_overlaps = []
        front_overlaps = []
        prices = []
        latitudes = []
        longitudes = []

        # Obtaining inputs from csv file and adding them to their associated lists
        import csv
        datafile = open('/FlightOptions.csv', 'r')
        filereader = list(csv.reader(datafile))

        for record in filereader:
            # the if statement makes sure the header row in the csv is not stored in the lists (CP)
            if record[0] != "Altitude (m)":
                altitudes.append(record[0])
                focal_lengths.append(record[1])
                x_sensor_lengths.append(record[2])
                y_sensor_lengths.append(record[3])
                survey_area_width.append(record[4])
                survey_area_length.append(record[5])
                side_overlaps.append(record[6])
                front_overlaps.append(record[7])
                prices.append(record[8])
                latitudes.append(record[9])
                longitudes.append(record[10])
            
        datafile.close()

        ################################## End of Inputs, Start of Calculations ###################################
        # Empty lists for all of our calculated values
        aerial_photo_footprints = []
        num_flight_lines = []
        flight_line_spacing = []
        num_images = []
        total_cost = []

        # Calculating aerial photo footprint for each record and adding it to its list
        for index in range (len(altitudes)):
            AerialPhotoFootprint = aerialphotosize(altitudes[index], focal_lengths[index], x_sensor_lengths[index], y_sensor_lengths[index])
            aerial_photo_footprints.append(AerialPhotoFootprint)

        # Calculating Number of Flight Lines for each record and adding it to its list
        for index in range (len(altitudes)):
            NumberofFlightLines = numflightlines(altitudes[index], focal_lengths[index], y_sensor_lengths[index], side_overlaps[index], survey_area_width[index])
            num_flight_lines.append(NumberofFlightLines)

        # Calculating Spacing of Flight Lines for each record and adding it to its list
        for index in range (len(altitudes)):
            Spacing = flightlinespacing(altitudes[index], focal_lengths[index], y_sensor_lengths[index], side_overlaps[index])
            flight_line_spacing.append(Spacing)

        # Calculating Total Number of Images for each record and adding it to its list
        for index in range (len(altitudes)):
            NumImages = numimages(altitudes[index], focal_lengths[index], x_sensor_lengths[index], front_overlaps[index], survey_area_length[index], num_flight_lines[index])
            num_images.append(NumImages)

        # Calculating Total Cost for each record and adding it to its list
        for index in range (len(altitudes)):
            TotalCost = totalcost(num_images[index], prices[index])
            total_cost.append(TotalCost)

        ################################## End of Calculations, Start of Outputs ###################################
        # Creating a new csv file to write the final data into
        SurveyOptions = open('FinalSurveyOptions.csv', 'w', newline="")
        filewriter = csv.writer(SurveyOptions)
        filewriter.writerow(["Aerial Footprint Size (m^2)","Number of Flight Lines","Number of Images","Total Cost ($)","Latitude","Longitude"])

        # Collecting Data from lists and writing it to file
        for index in range(len(total_cost)):
            filewriter.writerow([aerial_photo_footprints[index], num_flight_lines[index], num_images[index], total_cost[index], latitudes[index], longitudes[index]])

        SurveyOptions.close()


        # call the function to plot our flight to turtle
        plot_answer = input("Would you like the first survey plotted? (Y/N): ")
        if plot_answer.capitalize() == "Y":
            plotflight(num_flight_lines[0], survey_area_length[0], survey_area_width[0], latitudes[0], longitudes[0])

        print()
        print("Done - Your results have been saved to FinalSurveyOptions.csv")        

    if __name__ == '__main__':
        main()

# Executes if error in the try block
except IndentationError:
    print("Please check the indentation in the code.")  

except ValueError:
    print("Strings cannot be converted to float.")

except NameError:
    print("One of the variables is not defined.")

except ZeroDivisionError:
    print("Division by zero is not possible.")     

except FileNotFoundError:
    print("CSV input file not found.")

except AttributeError:
    print("Failed attribute reference, assignment, or append.")    

except IndexError:
    print("List index is out of range.")

except OverflowError:
    print("An arithmetic operation has exceeded the limits or is giving invalid results.")     

except Exception as message:
    print("Error: ",message)

print("-----------------------------------------")
print("Thank you for using this Drone Survey Planner!")
print("-----------------------------------------")

# Assumptions: 1. Users of the system have applied to operate drones beyond operators’ line of sight (BLOS) if applicable. 
#   2. The survey area terrain is flat, and drone altitude does not change throughout survey. 
#   3. The drone can complete the survey irrespective of the area that needs to be surveyed

# Limitations: 1. This application cannot be used in areas with varying elevation.
#   2. This application is only useful for rectangular Survey areas.
#   3. This application plots only the first survey in the csv. file if its not altered.

# References: DIY Drones [Blog entry by ‘unnamed idea’]. Preparing Auto Missions Using Python. (2016, January 28). Retrieved from https://diydrones.com/profiles/blogs/preparing-auto-missions-using-python. 
#   Leica Geosystems. (2005). Theodolites & Total Stations – Precision in Large-Scale Measurement. Moenchmattweg, Switzerland.  
#   Kateryna. (May 29, 2017). 5 things to know about drone data accuracy. Medium. Retrieved from https://medium.com/@kateryna_93325/5-things-to-know-about-drone-data-accuracy-92098aae48f7. 
#   SiteSee. (2021, June). Fluctuating Capture Altitude / Height Measurements Inaccurate. Retrieved from https://learn.sitesee.io/hc/en-us/articles/360052002592-Fluctuating-Capture-Altitude-Height-Measurements-Inaccurate. 
#   Stubbs, N. (n.d.) Camera sensor sizes compared. All Things Photography. Retrieved from https://www.all-things-photography.com/blog/camera-sensor-sizes-compared/. 
#   Zeeff, D. J. (December 5, 2018) DJI drone sensor size comparison page. DJZ Photography. Retrieved from https://www.djzphoto.com/blog/2018/12/5/dji-drone-quick-specs-amp-comparison-page. 