import cv2
import face_recognition
import numpy as np
import os
import pickle
from typing import List, Tuple, Optional

class FaceRecognizer:
    def __init__(self, model_path="models/face_encodings.pkl"):
        self.model_path = model_path
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()
    
    def load_known_faces(self):
        """Load known face encodings from pickle file"""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data['encodings']
                    self.known_face_names = data['names']
                print(f"Loaded {len(self.known_face_names)} known faces")
            except Exception as e:
                print(f"Error loading face encodings: {e}")
                self.known_face_encodings = []
                self.known_face_names = []
        else:
            print("No existing face encodings found")
    
    def save_known_faces(self):
        """Save known face encodings to pickle file"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        try:
            data = {
                'encodings': self.known_face_encodings,
                'names': self.known_face_names
            }
            with open(self.model_path, 'wb') as f:
                pickle.dump(data, f)
            print("Face encodings saved successfully")
        except Exception as e:
            print(f"Error saving face encodings: {e}")
    
    def add_new_face(self, image_path: str, name: str) -> bool:
        """Add a new face to the known faces database"""
        try:
            # Load the image
            image = face_recognition.load_image_file(image_path)
            
            # Get face encodings
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 0:
                print("No face found in the image")
                return False
            
            if len(face_encodings) > 1:
                print("Multiple faces found. Please use an image with only one face")
                return False
            
            # Add the face encoding and name
            face_encoding = face_encodings[0]
            
            # Check if person already exists
            if name in self.known_face_names:
                print(f"Person {name} already exists. Updating encoding...")
                index = self.known_face_names.index(name)
                self.known_face_encodings[index] = face_encoding
            else:
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(name)
            
            # Save the updated encodings
            self.save_known_faces()
            print(f"Successfully added/updated face for {name}")
            return True
            
        except Exception as e:
            print(f"Error adding face: {e}")
            return False
    
    def recognize_faces_in_frame(self, frame) -> List[Tuple[str, Tuple[int, int, int, int], float]]:
        """
        Recognize faces in a video frame
        Returns: List of tuples (name, (top, right, bottom, left), confidence)
        """
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        recognized_faces = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            
            name = "Unknown"
            confidence = 0
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    confidence = 1 - face_distances[best_match_index]
            
            # Scale back up face locations
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            recognized_faces.append((name, (top, right, bottom, left), confidence))
        
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
        
        while photos_taken < num_photos:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read from camera")
                break
            
            # Display the frame
            cv2.imshow(f'Capturing photos for {name} - {photos_taken}/{num_photos}', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):  # Space key to capture
                # Save the photo
                photo_path = os.path.join(face_dir, f"{name}_{photos_taken + 1}.jpg")
                cv2.imwrite(photo_path, frame)
                print(f"Photo {photos_taken + 1} captured")
                photos_taken += 1
            elif key == 27:  # ESC key to cancel
                print("Capture cancelled")
                cap.release()
                cv2.destroyAllWindows()
                return False
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Process the captured images to create face encodings
        return self.process_captured_images(name, face_dir)
    
    def process_captured_images(self, name: str, face_dir: str) -> bool:
        """Process captured images to create face encodings"""
        encodings = []
        
        for filename in os.listdir(face_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(face_dir, filename)
                
                try:
                    image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(image)
                    
                    if len(face_encodings) == 1:
                        encodings.append(face_encodings[0])
                    else:
                        print(f"Warning: Found {len(face_encodings)} faces in {filename}")
                
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        if not encodings:
            print("No valid face encodings found")
            return False
        
        # Average the encodings for better accuracy
        average_encoding = np.mean(encodings, axis=0)
        
        # Add to known faces
        if name in self.known_face_names:
            index = self.known_face_names.index(name)
            self.known_face_encodings[index] = average_encoding
        else:
            self.known_face_encodings.append(average_encoding)
            self.known_face_names.append(name)
        
        self.save_known_faces()
        print(f"Successfully processed {len(encodings)} images for {name}")
        return True
    
    def remove_person(self, name: str) -> bool:
        """Remove a person from the known faces database"""
        if name in self.known_face_names:
            index = self.known_face_names.index(name)
            del self.known_face_names[index]
            del self.known_face_encodings[index]
            self.save_known_faces()
            print(f"Removed {name} from database")
            return True
        else:
            print(f"{name} not found in database")
            return False
    
    def get_known_names(self) -> List[str]:
        """Get list of all known person names"""
        return self.known_face_names.copy()
