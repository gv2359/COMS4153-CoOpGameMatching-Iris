## Iris: Co-Op Game Matching Gateway

**Iris** is a microservice that acts as a gateway to all services in the Gamezon ecosystem. The UI service interacts solely with Iris, which then connects to the MatchService, NotificationService, and UserValidationService. This architecture streamlines user interactions and ensures efficient communication between services, enabling a seamless experience for gamers seeking partners for two-player cooperative games.

## Running the Application

To set up and run the Iris microservice, follow these steps:

1. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install the Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

5. **Access the API Documentation**:
   Navigate to `http://127.0.0.1:8001/docs` in your web browser to view and interact with the API endpoints.