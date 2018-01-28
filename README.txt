CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Requirements
 * Installation
 * Maintainers


INTRODUCTION
------------

The GigBag app launches a website hosted locally that uses command line
arguments to search a specific tour or concert on setlist.fm and creates
a Spotify playlist of the resulting set.

 * For source code:
   https://github.com/carsonclarke570/BrickHack4


REQUIREMENTS
------------

This module requires the following modules:

 * Flask

INSTALLATION
------------

 * To run the program:
        1) Run either:
            - python gig_bag.py -c [artist] [date] [venue]
                * artist: name of the artist you want to find a setlist for
                * date: date of the concert
                * venue: venue of the concert
            - python gig_bag.py -t [artist] [tour]
                * artist: name of the artist you want to find a setlist for
                * tour: name of the tour the artist performed
        2) 127.0.0.1:8080 in your web browser and hit "Create"
        3) Spotify wil request authorization
        4) After a confirmation page loads, check your Spotify account for
           the new playlist!

 * WARNING: The code can run slowly sometimes. Be patient.

MAINTAINERS
-----------

Current maintainers:
 * Carson Clarke-Magrab
 * Eric Kanis

This project was created for BrickHack 4:
 * BrickHack 4
   https://brickhack.io/