# Blockhouse Stock Fetcher App

## Overview
The Blockhouse Stock Fetcher App is a Django-based backend system designed to fetch financial data from a public API, implement a backtesting module, and generate reports with performance results. This project is primarily focused on Django development, API integration, and deployment.

## Extended Description
The **Blockhouse Stock Fetcher App** is a robust Django-based backend application designed to streamline the process of fetching, analyzing, and reporting financial data, specifically stock prices. With an emphasis on leveraging real-time data from the Alpha Vantage API, the application provides users with tools to perform comprehensive financial analysis through features like backtesting and predictive modeling.

### Key Features

- **Financial Data Fetching**: The application retrieves daily stock prices and relevant financial metrics using the Alpha Vantage API. Users can specify stock symbols to fetch the latest data and historical trends.

- **Backtesting Module**: Users can test trading strategies by simulating buy and sell actions based on historical data. The backtesting module evaluates user-defined parameters such as moving averages and initial investment amounts, providing insights into potential returns and performance metrics.

- **Predictive Analytics**: The integration of a pre-trained machine learning model allows users to predict future stock prices based on historical trends. This feature simplifies the complexity of machine learning, focusing on delivering actionable insights rather than requiring in-depth understanding or training of models.

- **Reporting Capabilities**: The app generates detailed reports that include performance summaries, visual comparisons of predicted vs. actual prices, and key financial metrics. Reports can be generated in various formats, making it easy for users to share and analyze results.

### Technical Implementation

- The application is built using **Django**, a high-level Python web framework that promotes rapid development and clean design. The choice of Django ensures scalability and a robust architecture.
  
- **PostgreSQL** serves as the relational database management system, offering reliability and efficiency for storing financial data. The use of Django ORM simplifies database interactions and schema management.

- The entire application is containerized using **Docker** and orchestrated with **Docker Compose**, facilitating easy deployment and environment consistency. This approach allows for seamless local development and production setups.

- **GitHub Actions** is integrated for continuous integration and deployment (CI/CD). This automation ensures that any changes made to the main branch are automatically built and deployed to an AWS EC2 instance, streamlining the development workflow and minimizing downtime.

### EC2 Instance Setup and RDS Integration

1. **Setting Up the EC2 Instance**: 
   - Launch an EC2 instance from the AWS Management Console. Choose an appropriate instance type based on your expected workload (e.g., t2.micro for testing).
   - Ensure that the security group associated with the instance allows inbound traffic on the necessary ports (e.g., 8081 for the application).

2. **Linking the RDS Instance**:
   - Create a PostgreSQL database instance in Amazon RDS. Set the database name to `blockhouse-db` and configure the user and password as specified in your `.env` file.
   - In the RDS settings, ensure that the security group allows inbound traffic from your EC2 instance's IP address.
   - Use the RDS endpoint as the `DB_HOST` variable in your `.env` file to establish the connection between the Django application running on EC2 and the PostgreSQL database.

### Future Enhancements

Future iterations of the Blockhouse Stock Fetcher App could include features such as:

- User authentication and authorization to provide personalized experiences.
- An intuitive frontend interface to visualize data and enhance user interaction.
- More complex machine learning algorithms for improved predictive accuracy.
- Integration with other financial APIs for broader data coverage and insights.

By combining powerful backend processing with user-friendly features, the Blockhouse Stock Fetcher App aims to become an essential tool for both novice and experienced investors looking to make informed financial decisions.

## Technologies Used
- Django: Version 5.1.2
- PostgreSQL: Used for relational database management
- Docker: Containerization of the application
- GitHub Actions: CI/CD for automated deployment
- Alpha Vantage API: For fetching financial data
- Various Python libraries: `pandas`, `numpy`, `matplotlib`, `scikit-learn`, etc.

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Docker and Docker Compose installed on your machine
- Access to an AWS account with RDS

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
4. Make sure the security group allows inbound traffic from your EC2 instance's IP address.
5. Note down the RDS endpoint, and use it to set the `DB_HOST` variable in your `.env` file.

### Building and Running the Application
1. Ensure you have Docker installed and running.
2. Build the Docker images and start the containers using Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

3. To access the application, visit `http://<your_ec2_instance_ip>:8081`.

## API Endpoints
- **Home**: `GET /` - Welcome message.
- **Fetch Stock Data**: `GET /stocks/fetch/?symbol=<stock_symbol>` - Fetch stock data for a specific symbol.
- **Backtest**: `GET /stocks/backtest/?symbol=<stock_symbol>&initial_investment=<amount>&short_window=<days>&long_window=<days>` - Perform backtesting on the given stock.
- **Predict**: `GET /stocks/predict/?symbol=<stock_symbol>&days=<number_of_days>` - Predict future stock prices.
- **Report**: `GET /stocks/report/?symbol=<stock_symbol>` - Generate a report including backtest results and predictions.

## Running Tests
To run the tests, execute the following command:
```bash
docker-compose run web python manage.py test
```

## Deployment
This project uses GitHub Actions for continuous integration and deployment. Upon pushing to the main branch, the application is automatically built and deployed to an EC2 instance.

## Troubleshooting
- Ensure that your `.env` variables are set correctly.
- Check that your RDS instance is accessible from your EC2 instance.
- Ensure the correct permissions are set for your EC2 key file.

## Conclusion
The Blockhouse Stock Fetcher App is a comprehensive tool for fetching, analyzing, and reporting stock data. Follow the above steps to set up and run the application.
