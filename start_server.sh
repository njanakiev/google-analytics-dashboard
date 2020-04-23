# Get environment variables
source .env

# Remove all __pycache__ folders
find . -type d -name __pycache__ -exec rm -r {} \+

if [ "$1" = "-b" ]; then
  echo "Build docker image"
  sudo docker build \
    -t google-analytics-dashboard .
fi

sudo docker run -it \
  -p 8050:8050 \
  -e VIEW_ID=$VIEW_ID \
  -v $KEY_FILE_LOCATION:/app/client_secrets.json \
  google-analytics-dashboard
