# Cryptographic Bit Randomness Validator

The Gitlab project can be accessed [here](https://gitlab.cs.pub.ro/andrei.ragman/imagetolatex).

The **Cryptographic Bit Randomness Validator** is a Python-based web application designed to evaluate the unpredictability of bit sequences. This is crucial for ensuring cryptographic security by adhering to NIST standards for randomness testing. The application features a user-friendly web interface, powerful backend statistical tools, and Dockerized deployment.

## Repository Migration
This project was initially developed on GitLab and has been migrated to GitHub by [silviaberescu](https://github.com/silviaberescu). The history and contributions of all team members are preserved in this repository.

## Project Features

- **User-Friendly Web Interface**: Simplifies the process of uploading bit sequences and reviewing detailed randomness analysis results.
- **NIST-Compliant Statistical Tests**: Includes Monobit, M-bit, Runs, Autocorrelation, and Serial Tests for comprehensive randomness evaluation.
- **Cryptographic Key Storage**: Securely stores and associates cryptographic keys with specific test results for auditing purposes.
- **Containerized Deployment**: Ensures consistent performance across environments using Docker.

## Rough Project Structure

```bash
cryptographic-validator/
├── web/                       # Flask web application
│   ├── static/                # Static js scripts and css stylesheets
│   ├── templates/             # Jinja templates
│   ├── app.py                 # Main server logic
│   ├── history_db.py          # Interactions with the SQL server for history
│   ├── request_results.py     # Interactions with the other container that runs the statistical tests
│   ├── upload.py              # Auxiliary method for uploading
│   ├── user_logging.py        # Handles authentication
│   ├── requirements.txt
│   └── Dockerfile
├── nist/                     # Statistical tests module
│   ├── stattests/
│   │   ├──
│   │   ├── monobit.py
│   │   ├── mbit.py
│   │   ├── runs.py
│   │   ├── autocorrelation.py
│   │   └── serial.py
│   ├── handle_requests.txt
│   ├── requirements.txt
│   └── Dockerfile.model
├── database/                  # Persistent data storage
├── docker-compose.yml         # Multi-container orchestration
└── README.md
```

## Development Workflow

1. **Branching and Merge Requests**:
   - Each developer works on their own branch.
   - After completing a task, create a Merge Request (MR) to the `main` branch.
   - All team members must review the MR, provide feedback, and approve before merging.
   - Use the `merge_request` template for every MR.

2. **Review Rules**:
   - No merging without unanimous approval (all team members must approve).
   - Address all review comments before merging.

## Setup and Running

### Steps to Run
1. Clone the repository:
   ```bash
   git clone https://gitlab.cs.pub.ro/andrei.ragman/imagetolatex.git
   cd imagetolatex # old name of the project haha
   ```

2. Start the application using Docker Compose:
   ```bash
   ./local.sh
   ```

3. Access the application in your browser at:
   ```
   http://localhost:5000
   ```

### For development only
- Docker and Docker Compose installed
- Use `pipreqs` to generate `requirements.txt`:
  ```bash
  pipreqs --force .
  ```

## API Interaction

The web service interacts with the backend using RESTful HTTP endpoints. For instance:
- **Predict Randomness**: Sends a bit sequence to the statistical tests module and returns results.
  ```
  GET http://nist:5001/compute?model_name=mbit&bit_string=110001011&significance=0.05
  ```

## Testing Strategy

- **Manual Testing**: Ensure the interface usability and correctness of statistical calculations.
- **Future Scope**: Expand to automated testing when time permits.

## Technologies Used

- **Languages**: Python (backend and statistical analysis), HTML/CSS/TypeScript (frontend)
- **Frameworks**: Flask (web backend)
- **Containerization**: Docker and Docker Compose for deployment and environment management.

## Future Enhancements

- Add a database of pre-tested sequences for reference.
- Incorporate automated testing workflows for reliability.
- Add HTTPS support for secure communication.


## Individual Contributions

### Răgman Andrei-Adrian
- Established the project structure and configured GitLab CI/CD pipelines for linting and generating `requirements.txt` files.
- Developed and implemented the statistical tests.
- Configured Docker containers and utilized `docker-compose` for container orchestration.
- Created the logic for submission results and data storage.
- Enhanced the SQL server by adding an additional table to store submission history.
- Supervised the progress of team members, providing assistance with Git and resolving other arising issues.

### Berescu Silvia-Maria 
- Developed and Implemented the Web Interface. Created reusable templates with Jinja, dynamic content blocks, 
and navigation routes in app.py.
- Styled the Project, using CSS and JavaScript for consistent design, hover effects, and transitions.
- Built a results table with filtering logic for history.
- Designed input forms for statistical tests with dynamic fields and links to documentation.
- Added styled pages for tests and enabled redirects from the upload page.
- Implemented delete functionality for history results entries.
- Added logout option.

### Alexe Mihail
TODO @alexe

## Problems we stumbled upon

Silvia: Encountered issues while configuring routes and rendering templates in app.py, which were resolved through debugging, 
team discussions and troubleshooting. Faced merge conflicts during collaborative development but successfully resolved them by coordinating with colleagues and reviewing code changes.