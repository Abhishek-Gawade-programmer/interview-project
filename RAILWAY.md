# Deploying to Railway.app

This guide explains how to deploy this FastAPI application to Railway.app.

## Prerequisites

1. Create an account on [Railway.app](https://railway.app)
2. Install the Railway CLI: `npm i -g @railway/cli`
3. Login to Railway using the CLI: `railway login`

## Deployment Steps

1. Initialize your project (if not already done): `railway init`
2. Provision a new PostgreSQL database (optional):

   ```
   railway add
   ```

   Select PostgreSQL from the list of plugins.

3. Set up environment variables:

   ```
   railway variables set OPENAI_API_KEY=your_openai_api_key
   railway variables set SQLALCHEMY_DATABASE_URI=${{ Postgres.DATABASE_URL }}
   ```

4. Deploy your application:

   ```
   railway up
   ```

5. Check the status of your deployment:

   ```
   railway status
   ```

6. Open your application in the browser:
   ```
   railway open
   ```

## Configuration

The application is configured to:

1. Use the Dockerfile for building the container
2. Run database migrations automatically on startup
3. Start the application with Hypercorn using 2 worker processes
4. Use the `/health` endpoint for Railway's health checks

## Monitoring and Logs

To view logs of your deployment:

```
railway logs
```

## Environment Variables

Make sure to set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key for the RAG pipeline
- `SQLALCHEMY_DATABASE_URI`: Connection string for your database
- `SECRET_KEY`: Secret key for JWT token generation
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

## Troubleshooting

If you encounter any issues with the deployment:

1. Check the logs: `railway logs`
2. Verify your environment variables: `railway variables`
3. Restart the deployment: `railway up`
