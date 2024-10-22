# Use a full-featured Python image as a base
FROM python:3.9-slim

# Install necessary packages for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libxss1 \
    libgconf-2-4 \
    libxi6 \
    libxrender1 \
    libxrandr2 \
    libgtk-3-0 \
    libgbm-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O /tmp/google-chrome.deb https://dl.google.com/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb \
    && apt-get update \
    && apt-get install -y /tmp/google-chrome.deb \
    && rm /tmp/google-chrome.deb \
    && apt-get clean

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '[\d\.]+') \
    && CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION) \
    && wget -q -O /usr/local/bin/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip /usr/local/bin/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /usr/local/bin/chromedriver.zip

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Command to run your application
CMD ["python", "monitor.py"]
