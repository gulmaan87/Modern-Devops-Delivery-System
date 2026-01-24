from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

# now initializing the app
app = FastAPI(
    title = "DevOps Delivery System API",
    Description = "backend API for mordern DevOps System",
    version="1.0.0"
)
#cors Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins =os.getenv("CORS_ORIGINS","http://localhost:3000").split(","),
    allow_credentials = True,
    allow_methods = ["*"],
    allow_header = ["*"],
    
)

# Connect to MongoDB Atlas on startup
@app.on_event("startup")
async def startup_db_client():
    """Connect to MongoDB Atlas on application startup"""
    global mongodb_client, mongodb_db
    try:
        # Get MongoDB Atlas connection string from environment variable
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            print("⚠️  WARNING: DATABASE_URL not set. MongoDB connection will fail.")
            return
        
        # Connect to MongoDB Atlas
        mongodb_client = AsyncIOMotorClient(database_url)
        mongodb_db = mongodb_client.get_database()
        
        # Test connection
        await mongodb_client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully")
    except ConnectionFailure as e:
        print(f"❌ MongoDB Atlas connection error: {e}")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB Atlas: {e}")

# Close MongoDB connection on shutdown
@app.on_event("shutdown")
async def shutdown_db_client():
    """Close MongoDB Atlas connection on application shutdown"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        print("MongoDB Atlas connection closed")

#health Check Endpoint(reqire for K8S)
@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes and monitoring"""
    db_status = "disconnected"
    try:
        if mongodb_client:
            await mongodb_client.admin.command('ping')
            db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "backend-api",
        "database": db_status,
        "database_type": "MongoDB Atlas"
    }
    
    #root Endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
             "message":"Welcome to DevOps Delivery System API",
             "version": "1.0.0",
             "docs":"/docs"
             
         }
         
         #API endpoint
@app.get("/api/status")
async def get_status():
    """Get API status"""
    db_connected = False
    try:
        if mongodb_client:
            await mongodb_client.admin.command('ping')
            db_connected = True
    except:
        db_connected = False
    
    return {
        "status": "operational",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database_connected": db_connected,
        "database_type": "MongoDB Atlas"
    }
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT",8000))
    uvicorn.run(app,host="0.0.0.0",port=port)    