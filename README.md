Auto scale SABnzbd based on the free disk space of your system, entirely using the SAB api.

This is designed for systems where you may be downloading things which are moved off the primary disk quickly, such as when using Radarr or Sonarr.

To get started, clone the repo, install the requirements, and copy config.example.py to config.py. Fill out the values in config.py for your system, and then run main.py. If successful, you should be able to check SAB, and see the throttling in prqctice:
