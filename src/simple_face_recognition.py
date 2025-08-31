"""
Facial Recognition Attendance System - Face Recognition Module
Author: Uzman Jawaid
Description: OpenCV-based face detection and recognition using Haar Cascades
Version: 2.0
Date: August 2025
"""

import cv2
import numpy as np
import os
import pickle
from typing import List, Tuple, Optional
import hashlib

class SimpleFaceRecognizer:
    """
    Simplified face recognizer using OpenCV's built-in face detection
    This version uses template matching and can be upgraded to use 
    more advanced face recognition libraries when available.
    """
    
    def __init__(self, model_path="models/face_templates.pkl"):
        self.model_path = model_path
        self.face_templates = {}
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.load_face_templates()
    
    def load_face_templates(self):
        """Load face templates from pickle file"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.face_templates = pickle.load(f)
                print(f"Loaded {len(self.face_templates)} face templates")
            except Exception as e:
                print(f"Error loading face templates: {e}")
                self.face_templates = {}
        else:
            print("No existing face templates found")
    
    def save_face_templates(self):
        """Save face templates to pickle file"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        try:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.face_templates, f)
            print("Face templates saved successfully")
        except Exception as e:
            print(f"Error saving face templates: {e}")
    
    def extract_face_features(self, face_roi):
        """Extract simple features from face ROI"""
        # Resize to standard size
        face_roi = cv2.resize(face_roi, (100, 100))
        
        # Convert to grayscale if needed
        if len(face_roi.shape) == 3:
            face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        
        # Calculate histogram as a simple feature
        hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
        hist = hist.flatten()
        
        # Normalize
        hist = hist / (hist.sum() + 1e-7)
        
        return hist
    
    def compare_faces(self, features1, features2):
        """Compare two face feature vectors"""
        # Use correlation coefficient as similarity measure
        correlation = cv2.compareHist(features1, features2, cv2.HISTCMP_CORREL)
        return correlation
    
    def add_new_face(self, image_path: str, name: str) -> bool:
        """Add a new face to the templates database"""
        try:
            # Load the image
            image = cv2.imread(image_path)
            if image is None:
                print("Could not load image")
                return False
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                print("No face found in the image")
                return False
            
            if len(faces) > 1:
                print("Multiple faces found. Please use an image with only one face")
                return False
            
            # Extract face ROI
            x, y, w, h = faces[0]
            face_roi = gray[y:y+h, x:x+w]
            
            # Extract features
            features = self.extract_face_features(face_roi)
            
            # Store template
            self.face_templates[name] = {
                'features': features,
                'face_roi': face_roi
            }
            
            # Save templates
            self.save_face_templates()
            print(f"Successfully added face template for {name}")
            return True
            
        except Exception as e:
            print(f"Error adding face: {e}")
            return False
    
    def recognize_faces_in_frame(self, frame) -> List[Tuple[str, Tuple[int, int, int, int], float]]:
        """
        Recognize faces in a video frame using simple template matching
        Returns: List of tuples (name, (x, y, w, h), confidence)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        recognized_faces = []
        
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            face_features = self.extract_face_features(face_roi)
            
            best_match = "Unknown"
            best_confidence = 0
            
            # Compare with all templates
            for name, template in self.face_templates.items():
                confidence = self.compare_faces(face_features, template['features'])
                
                if confidence > best_confidence and confidence > 0.6:  # Threshold
                    best_confidence = confidence
                    best_match = name
            
            # Convert to expected format (top, right, bottom, left)
            recognized_faces.append((best_match, (y, x+w, y+h, x), best_confidence))
        
        return recognized_faces
    
    def capture_face_for_training(self, name: str, num_photos: int = 5) -> bool:
        """Capture multiple photos of a person for training"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return False
        
        # Create directory for storing face images
        face_dir = f"data/faces/{name}"
        os.makedirs(face_dir, exist_ok=True)
        
        photos_taken = 0
        print(f"Capturing {num_photos} photos for {name}")
        print("Press SPACE to capture photo, ESC to cancel")
        
        templates = []
        
        while photos_taken < num_photos:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read from camera")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # Draw rectangles around detected faces
            display_frame = frame.copy()
            for (x, y, w, h) in faces:
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            cv2.putText(display_frame, f"Photos: {photos_taken}/{num_photos}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(display_frame, "SPACE: Capture, ESC: Cancel", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow(f'Capturing photos for {name}', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space key to capture
                if len(faces) == 1:
                    # Save the photo
                    photo_path = os.path.join(face_dir, f"{name}_{photos_taken + 1}.jpg")
                    cv2.imwrite(photo_path, frame)
                    
                    # Extract face template
                    x, y, w, h = faces[0]
                    face_roi = gray[y:y+h, x:x+w]
                    features = self.extract_face_features(face_roi)
                    templates.append(features)
                    
                    print(f"Photo {photos_taken + 1} captured")
                    photos_taken += 1
                else:
                    print("Please ensure exactly one face is visible")
                    
            elif key == 27:  # ESC key to cancel
                print("Capture cancelled")
                cap.release()
                cv2.destroyAllWindows()
                return False
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Average the templates
        if templates:
            avg_template = np.mean(templates, axis=0)
            self.face_templates[name] = {
                'features': avg_template,
                'face_roi': None  # We don't need to store the ROI for averaged templates
            }
            self.save_face_templates()
            print(f"Successfully processed {len(templates)} photos for {name}")
            return True
        else:
            print("No valid face templates captured")
            return False
    
    def remove_person(self, name: str) -> bool:
        """Remove a person from the templates database"""
        if name in self.face_templates:
            del self.face_templates[name]
            self.save_face_templates()
            print(f"Removed {name} from database")
            return True
        else:
            print(f"{name} not found in database")
            return False
    
    def get_known_names(self) -> List[str]:
        """Get list of all known person names"""
        return list(self.face_templates.keys())
