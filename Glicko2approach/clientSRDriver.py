"""
Owner: Dan Birmingham
Contributers:
Start date: Dec 12 2019
Last updated:Dec 12 2019
Description: Application designed to leverage drive interactions with and updates
to a sailing ranking database using the glicko2 protocol

Licensing: 

dependencies
system:     

python:     glicko2: "INSERT GIT ADDRESS" (nested)
			SailingGlicko2
            csv
           
"""
from SailingGlicko2 import *
import csv


################################################################################
## Notes #######################################################################
################################################################################

#Probably store a database offline somehow in a file. Then when the database
#needs to be updated, we can read from and write to that offline file. Eventually
#if we got to a database, users can get preliminary updated rankings from the 
#database but also request official updates.