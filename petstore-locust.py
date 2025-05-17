import os
import uuid
import logging
from locust import HttpUser, task, between
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ApiUser(HttpUser):
    wait_time = between(1, 3)
    host = os.getenv("BASE_URL", "https://petstore3.swagger.io/api/v3")
    timeout_duration = 90
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'True') == 'True'
    api_key = os.getenv("API_KEY", "12345")
    pet_id = None  # To store the dynamically generated pet ID

    def on_start(self):
        """Executed when a user starts running the test."""
        logging.info("Starting test scenario...")

    @task
    def run_scenario(self):
        """Run the sequence of operations."""
        self.create_pet()
        self.get_pet()
        self.update_pet()
        self.delete_pet()

    def create_pet(self):
        """Create a new pet."""
        self.pet_id = str(uuid.uuid4().int % 1000000)  # Generate a unique pet ID
        url = f"{self.host}/pet"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "api_key": self.api_key
        }
        payload = {
            "id": int(self.pet_id),
            "name": "Fluffy",
            "category": {"id": 1, "name": "Dogs"},
            "photoUrls": ["https://example.com/photo.jpg"],
            "tags": [{"id": 1, "name": "cute"}],
            "status": "available"
        }

        with self.client.post(
            url,
            headers=headers,
            json=payload,
            name="Create Pet",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
                logging.info(f"Pet created successfully with ID: {self.pet_id}")
            else:
                response.failure(f"Failed to create pet: {response.status_code}, {response.text}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {url}, Headers: {headers}, Payload: {payload}")

    def get_pet(self):
        """Retrieve the newly created pet."""
        url = f"{self.host}/pet/{self.pet_id}"
        headers = {
            "Accept": "application/json",
            "api_key": self.api_key
        }

        with self.client.get(
            url,
            headers=headers,
            name="Get Pet",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code == 200:
                response.success()
                logging.info(f"Pet retrieved successfully: {response.text}")
            else:
                response.failure(f"Failed to retrieve pet: {response.status_code}, {response.text}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {url}, Headers: {headers}")

    def update_pet(self):
        """Update the pet."""
        url = f"{self.host}/pet"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "api_key": self.api_key
        }
        payload = {
            "id": int(self.pet_id),
            "name": "UpdatedFluffy",
            "category": {"id": 1, "name": "Dogs"},
            "photoUrls": ["https://example.com/newphoto.jpg"],
            "tags": [{"id": 1, "name": "cute"}],
            "status": "sold"
        }

        with self.client.put(
            url,
            headers=headers,
            json=payload,
            name="Update Pet",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
                logging.info(f"Pet updated successfully: {response.text}")
            else:
                response.failure(f"Failed to update pet: {response.status_code}, {response.text}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {url}, Headers: {headers}, Payload: {payload}")

    def delete_pet(self):
        """Delete the pet."""
        url = f"{self.host}/pet/{self.pet_id}"
        headers = {
            "Accept": "application/json",
            "api_key": self.api_key
        }

        with self.client.delete(
            url,
            headers=headers,
            name="Delete Pet",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code in [200, 204]:
                response.success()
                logging.info(f"Pet deleted successfully with ID: {self.pet_id}")
            else:
                response.failure(f"Failed to delete pet: {response.status_code}, {response.text}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {url}, Headers: {headers}")

    def on_stop(self):
        """Clean up resources if necessary."""
        logging.info("Test scenario completed.")