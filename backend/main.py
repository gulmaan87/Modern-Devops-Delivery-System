from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Atlas connection variables
mongodb_client = None
mongodb_db = None

# Initialize FastAPI app
app = FastAPI(
    title="DevOps Delivery System API",
    description="Backend API for Modern DevOps Delivery System",
    version="1.0.0"
)

# CORS middleware - configure for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "https://moderndevopsdeleverysystem.netlify.app").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB Atlas on startup
@app.on_event("startup")
async def startup_db_client():
    """Connect to MongoDB Atlas on application startup"""
    global mongodb_client, mongodb_db
    try:
        # Get MongoDB Atlas connection string from environment variable
        database_url = os.getenv("MONGODB_ATLAS_URL")
        
        if not database_url:
            print("⚠️  WARNING: DATABASE_URL not set. MongoDB connection will fail.")
            return
        
        # Get database name from environment or use default
        database_name = os.getenv("MONGO_DB_NAME", "devopsdb")
        
        # Connect to MongoDB Atlas
        mongodb_client = AsyncIOMotorClient(database_url)
        
        # Get the database explicitly by name
        mongodb_db = mongodb_client[database_name]
        
        # Test connection
        await mongodb_client.admin.command('ping')
        print(f"✅ Connected to MongoDB Atlas successfully")
        print(f"📦 Using database: {database_name}")
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

# Health check endpoint (required for Kubernetes liveness/readiness probes)
@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes and monitoring"""
    global mongodb_client
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

# Root endpoint
@app.get("/")
@app.head("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to DevOps Delivery System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# API endpoint example
@app.get("/api/status")
async def get_status():
    """Get API status"""
    global mongodb_client
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
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)    
