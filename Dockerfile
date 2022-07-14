FROM python:3.9


# Update the system and install firefox
RUN apt-get update 
RUN apt -y upgrade 
RUN apt-get install -y firefox-esr

#Make the Working Directory
WORKDIR /user/src/app

COPY requirements.txt ./
COPY scraper_object.py ./
COPY CEX_scraping.py ./

# get the latest release version of firefox 
RUN latest_release=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest \
    | grep tag_name | sed -E 's/.*"([^"]+)".*/\1/') && \
    # Download the latest release of geckodriver
    wget https://github.com/mozilla/geckodriver/releases/download/$latest_release/geckodriver-$latest_release-linux32.tar.gz \
    # extract the geckodriver
    && tar -xvzf geckodriver* \
    # add executable permissions to the driver
    && chmod +x geckodriver \
    # Move gecko driver in the system path
    && mv geckodriver /usr/local/bin \
    #Install Requirements
    && pip install --no-cache-dir -r requirements.txt --user 

# enter entry point parameters executing the container
CMD ["python", "./CEX_scraping.py"] 

# exposing the port to match the port in the runserver.py file
EXPOSE 5432