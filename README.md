# google-analytics-dashboard

Simple dashboard for [Google Analytics](https://analytics.google.com) with [Dash](https://plotly.com/dash/), [Plotly](https://plotly.com/), Python and Docker

# Installation

The dashboard requires an `.env` file in the project folder where the `VIEW_ID` is set which you can find in your Google Analytics view:

```bash
VIEW_ID=123456789
```
Additionally the dashboard requires the access file `client_secrets.json` which you can download from Google Analytics.

Finally, you can build the project with:

```bash
docker-compose build
```

# Usage

To run the dashboard, type:

```bash
docker-compose up
```
Now the dashboard should be accessible at: `http://localhost:8050/`

# License 
This project is licensed under the MIT license. See the [LICENSE](LICENSE) for details.
