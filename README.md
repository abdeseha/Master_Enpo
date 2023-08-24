# Master_Enpo
  This peice of software allows characterizing or identiying an operation/cycle of a machine based on the 
consumed electrical power.
  The data folder holds the data where it should be in the form {time,I_1,I_2,I_3,V}
  The calculate.py file holds the clases "Calculate" tha is responsible for the calculations (the electric power "pow",
the mobile average "mob_avg" and the derivetive "div"):
- the pow function takes I_1, I_2, I3, and V if exist and give the power.
- the mob_avg takes the list of values, the number of values to average on and the number of time to do the average
(if 2 we do the mobile average of the mobile average).
- the div takes time, and the values and returns the dirivetives.

in addintion to the "Calculate" class we have "Characterize" that takes:
- the time values to get the instance when the operation/cycle starts or ends.
- the org_values (power) to get the highest value in the operation/cycle of the power.
- the meaned_values (the average of the power) to get the value in wich the operation stabelize
- the dives (dirivetives) to know when the operation start and ends with the help of the meand values.
it checks the stabilization value of each step to see if it's a new cycle of an old operation or a new operation.
it saves the data (the operations) in a dectionary in the form:
{"operation_1":{"nub_of_use":integer
                "stab_value":integer
                "start_time":[]
                "end_time":[]
                "max":[]
                }}
- the nub_of_use is the nubmer of cycles an operation.
- the stabe_value is the stavilization value of the operation (the criterion based on which we can say if it's a cycle of
an operation or a new operation )
- the start_time a list holds all the start time of all the cycles of an operation in order.
- the end_time a list holds all the end time of all the cycles of an operation in order.
- the max is a list holds all cycles of the operation max values.

the main.py is the one file to run, that hold the GUI and calls the other functions depends on the user.
  it has 4 mager functionalities Analyse (analyse the data and outputs the operations), Simulate (Simulate the mechine 'To Do'), Train ('To train the modal based on the result of Analyse'), Plan (wich give a scheduel based on the trained model)

  The 'Settings' has for the moments only the settings for the Analyse funcion.

the analyse file holds the functionality of the Analyse tab in the user interface.

you can find pictures form the app in the pics folder, and examples of the output data form the analyse function in the data folder.

This code is in python so first we insall python from 'https://www.python.org/downloads/' the used version is 3.11.4.
Next to install dependencies we first install pip:
- Fist check pip version by: pip --version
To install if it doesn't exist:
- For MacOs and Linux: python3 -m ensurepip --upgrade
- For Windows: python -m ensurepip --upgrade

finally to install all dependencies, run: pip install -r Requirements.txt