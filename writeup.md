# US Weather Data Mapping

![A screenshot of your application. Could be a GIF.](screenshot.png)

For this project I wanted to create visualizations that allow for the direct comparison of weather amongst different states in the continental United States. To do this I watned to create tools that allow different weather phenomenon such as temperature and precipitation to be directly compared between different states and analyzed thoroughly for individual states. 

## Project Goals

TODO: **A clear description of the goals of your project.** Describe the question that you are enabling a user to answer. The question should be compelling and the solution should be focused on helping users achieve their goals. 

The main goal of this project was to develop a tool that allows a user to compare the weather patterns of differnt states. I wanted to give users the oppurtunity to find where in the US they could expect to find their ideal weather based on a number of factors. 

## Design

TODO: **A rationale for your design decisions.** How did you choose your particular visual encodings and interaction techniques? What alternatives did you consider and how did you arrive at your ultimate choices?

The first endcoding I wanted to explore was a geographic heat map. I wanted to use this because the project involved comparing different states and found that maps were the best way to visualize states. Furthermore, weather is likely going to be more similar based on the spatial distance from each other. The map was a useful tool for seeing the general trends across the country, however, it was difficult to compare locations that were further apart from one another. This lead to the decision to build graphs that display the top or bottom n data points from the map based on user inputs. THe graph displays accompanying the map were challenging because at low n number of states to display there was very little difference between bars, but at high n number of states it becomes harder to read. This informed the deciison to allow a user to change these as they desired. 

The next portion of the project involves individually analyzing states based on their temperature. For this part of the project I wanted to explore temperature stability. Specifically, there were two things I wanteed to exlpore more in depth: how much the tempoeratrure changes within a day and how much does the temperature change between seasons throughout the year. For this portion of the project it made sense to focus only on a single state at a time to see how temperature changes over time. The two measured areas were the average temperature within a day and the difference betwwen maximum and minimum temperatures in a day, which created two different scatter plots which the user can select which to display at a time. The scatterplots suffered from having a lot of noise. Two updates were added to help solve the issue of noisy data. The first is to group the datapoints into bins for each month. The second was to add a treadline to the scatter plot to easily display the general trends in the data. 

## Development

TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time?

## Success Story

TODO:  **A success story of your project.** Describe an insight or discovery you gain with your application that relates to the goals of your project.
