# 1. Start with a lightweight Linux environment that has Python 3.11 installed
FROM python:3.11-slim

# 2. Tell the system we don't want interactive prompts freezing the build
ENV DEBIAN_FRONTEND=noninteractive

# 3. Install R and the necessary R packages 
# (We use pre-compiled r-cran-* binaries to save hours of compilation time)
RUN apt-get update && apt-get install -y \
    r-base \
    r-cran-tidyverse \
    r-cran-broom \
    && rm -rf /var/lib/apt/lists/*

# 4. Set the working directory inside our "virtual computer"
WORKDIR /app

# 5. Copy our requirements file and install the Python tools
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of our project files into the container
COPY . .

# 7. Tell Docker that Streamlit uses port 8501 to show the web app
EXPOSE 8501

# 8. Define the default command to run when the container starts
CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]