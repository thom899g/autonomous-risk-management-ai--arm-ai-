"""
Firebase Client for ARM AI State Management
Handles all Firebase Firestore operations for real-time state tracking
"""
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.base_query import FieldFilter
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os

from config import config

logger = logging.getLogger(__name__)

class FirebaseClient:
    """Firebase Firestore client for ARM AI state management"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize_firebase()
            self._initialized = True
    
    def _initialize_firebase(self) -> None:
        """Initialize Firebase connection with error handling"""
        try:
            if not firebase_admin._apps:
                if os.path.exists(config.FIREBASE.CREDENTIALS_PATH):
                    cred = credentials.Certificate(config.FIREBASE.CREDENTIALS_PATH)
                    firebase_admin.initialize_app(cred, {
                        'projectId': config.FIREBASE.PROJECT_ID
                    })
                    logger.info("Firebase initialized successfully")
                else:
                    logger.warning(f"Firebase credentials not found at {config.FIREBASE.CREDENTIALS_PATH}")
                    # Initialize without credentials for development (will fail on write)
                    firebase_admin.initialize_app()
            self.db = firestore.client()
            logger.info("Firestore client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            raise
    
    def log_risk_event(self, event_data: Dict[str, Any]) -> str:
        """
        Log a risk event to Firestore with timestamp and severity
        
        Args:
            event_data: Dictionary containing risk event details
            
        Returns:
            Document ID of the created event
        """
        try:
            event_data['timestamp'] = datetime.utcnow()
            event_data['processed'] = False
            
            doc_ref = self.db.collection(config.FIREBASE.RISK_EVENTS_COLLECTION).document()
            doc_ref.set(event_data)
            logger.info(f"Risk event logged: {event_data.get('type', 'unknown')}")
            return doc_ref.id
        except Exception as e:
            logger.error