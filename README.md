# Blockhouse Stock Fetcher App

## Overview
The Blockhouse Stock Fetcher App is a Django-based backend system designed to fetch financial data from a public API, implement a backtesting module, and generate reports with performance results. This project is primarily focused on Django development, API integration, and deployment.

## Technologies Used
- **Django**: Version 5.1.2
- **PostgreSQL**: Used for relational database management
- **Docker**: Containerization of the application
- **Docker Compose**: Simplifies the management of multi-container Docker applications
- **GitHub Actions**: CI/CD for automated deployment
- **Alpha Vantage API**: For fetching financial data
- **Various Python libraries**: 
  - `pandas`: Data manipulation and analysis
  - `numpy`: Numerical computing
  - `matplotlib`: Data visualization
  - `scikit-learn`: Machine learning
  - `requests`: HTTP requests for API calls
  - `python-dotenv`: Load environment variables from a `.env` file
  - `reportlab`: PDF generation for reports

## Setup Instructions

### Prerequisites
- **Python 3.10** or higher
- **Docker** and **Docker Compose** installed on your machine
- Access to an **AWS account** with RDS for database hosting

### Cloning the Repository
```bash
git clone https://github.com/LulzimTafaj/blockhouse_app.git
cd blockhouse_app
```

### Setting Up Environment Variables
Create a `.env` file in the root directory of the project and include the following environment variables:
```
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
DB_NAME=blockhouse-db
DB_USER=your_rds_username
DB_PASSWORD=your_rds_password
DB_HOST=your_rds_endpoint
DB_PORT=5432
DEBUG=True
EC2_HOST=your_ec2_instance_public_ip
EC2_KEY=your_base64_encoded_ec2_key
```

### Setting Up RDS (Amazon Relational Database Service)
1. Log in to the AWS Management Console.
2. Navigate to RDS and create a new PostgreSQL database instance.
3. Set the database name to `blockhouse-db`, and configure the user and password as specified in your `.env` file.
4. Ensure that the security group allows inbound traffic from your EC2 instance's IP address.
5. Note down the RDS endpoint and use it to set the `DB_HOST` variable in your `.env` file.

### Building and Running the Application
1. Ensure you have Docker installed and running.
2. Build the Docker images and start the containers using Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
3. To access the application, visit `http://<your_ec2_instance_ip>:8081`.

## API Endpoints
- **Home**: `GET /` - Displays a welcome message.
- **Fetch Stock Data**: `GET /stocks/fetch/?symbol=<stock_symbol>` - Fetches stock data for a specific symbol.
- **Backtest**: `GET /stocks/backtest/?symbol=<stock_symbol>&initial_investment=<amount>&short_window=<days>&long_window=<days>` - Performs backtesting on the given stock.
- **Predict**: `GET /stocks/predict/?symbol=<stock_symbol>&days=<number_of_days>` - Predicts future stock prices.
- **Report**: `GET /stocks/report/?symbol=<stock_symbol>` - Generates a report including backtest results and predictions.

## Running Tests
To run the tests, execute the following command:
```bash
docker-compose run web python manage.py test
```

## Deployment
This project uses GitHub Actions for continuous integration and deployment. Upon pushing to the main branch, the application is automatically built and deployed to an EC2 instance. Ensure that the necessary secrets (like database credentials and EC2 key) are configured in your GitHub repository.

## Troubleshooting
- Ensure that your `.env` variables are set correctly.
- Check that your RDS instance is accessible from your EC2 instance.
- Ensure the correct permissions are set for your EC2 key file.
- If the Docker container fails to start, check the logs using:
  ```bash
  docker-compose logs
  ```

## Conclusion
The Blockhouse Stock Fetcher App is a comprehensive tool for fetching, analyzing, and reporting stock data. Follow the above steps to set up and run the application. If you have any questions or issues, feel free to reach out for assistance.

## Additional Notes
- Ensure that all API keys and sensitive data are stored securely and are not hard-coded in the source code.
- The application is designed to be scalable; consider deploying with a load balancer if usage increases significantly.
