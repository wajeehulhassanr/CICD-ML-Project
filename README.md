# ML Project with CI/CD Pipeline

A machine learning project with a complete CI/CD pipeline that demonstrates best practices for MLOps.

## 📋 Project Overview

This project implements a simple machine learning application for Iris flower classification with a complete CI/CD pipeline for automated testing, deployment, and monitoring. It includes:

- Data loading and preprocessing
- Model training, testing, and prediction
- Flask API for serving the model
- Comprehensive CI/CD pipeline with GitHub Actions, Jenkins, and Docker

## 🚀 CI/CD Pipeline Architecture

```
GitHub Repository (3 branches)
│
├── dev branch ───────────┐
│   │                     │
│   │ ┌─────────────────┐ │
│   └▶│ Code Quality    │ │
│     │ Check (Flake8)  │ │
│     └─────────────────┘ │
│                         │
├── test branch ──────────┤
│   │                     │
│   │ ┌─────────────────┐ │
│   └▶│ Automated       │ │
│     │ Testing (pytest)│ │
│     └─────────────────┘ │
│                         │
└── master branch ────────┘
    │
    │ ┌───────────────────────┐
    └▶│ Jenkins Deployment    │
      │ - Build Docker        │
      │ - Push to Registry    │
      │ - Deploy Application  │
      │ - Admin Approval      │
      │ - Email Notification  │
      └───────────────────────┘
```

## 🛠️ Technology Stack

- **Language:** Python 3.9
- **ML Framework:** scikit-learn
- **API Framework:** Flask
- **Testing:** pytest
- **Code Quality:** Flake8
- **CI/CD:** GitHub Actions, Jenkins
- **Containerization:** Docker
- **Notification:** Email, Slack

## 🔄 Detailed Workflow & Requirements Implementation

This section explains in detail how each requirement is met and the workflow from development to production.

### 1. Repository Setup & Branching Strategy

The repository follows a three-branch strategy:

**Dev Branch (Development)**
- Purpose: Feature development and initial bug fixes
- Protection: No direct pushes to this branch; must go through pull requests
- Code Quality Check: Enforced via GitHub Actions

**Test Branch (Pre-Production)**
- Purpose: Validate features before deploying to production
- Protection: Only accept merges from `dev` branch that pass code quality checks
- Automated Testing: Complete test suite runs on this branch

**Master Branch (Production)**
- Purpose: Production-ready code only
- Protection: Only accept merges from `test` branch that pass all tests
- Deployment: Triggers Jenkins deployment pipeline

**Workflow Steps:**
1. Create feature branch from `dev` branch: `git checkout -b feature/new-feature dev`
2. Implement and test changes locally: `pytest tests/`
3. Push feature branch and create pull request to `dev`
4. GitHub Actions automatically runs Flake8 to ensure code quality
5. After code review and approval, merge to `dev`
6. Create pull request from `dev` to `test`
7. GitHub Actions runs the full test suite against the `test` branch
8. After tests pass and review, merge to `test`
9. Create pull request from `test` to `master`
10. After final review, merge to `master` to trigger deployment

### 2. Code Quality Enforcement

**Implementation:**
- GitHub Actions workflow: `.github/workflows/code_quality.yml`
- Triggered on: Push and pull requests to `dev` branch
- Tool: Flake8

**Configuration:**
```yaml
# Critical checks that will fail the build
flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics

# Style checks reported as warnings
flake8 src/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

**Workflow Steps:**
1. Developer pushes changes to a feature branch
2. Creates pull request to `dev` branch
3. GitHub Actions automatically triggers Flake8
4. PR can only be merged if Flake8 checks pass
5. Review the code quality report for any warnings

### 3. Automated Testing

**Implementation:**
- GitHub Actions workflow: `.github/workflows/feature_testing.yml`
- Triggered on: Push and pull requests to `test` branch
- Tool: pytest with coverage reporting

**Tests Cover:**
- Data loading: `test_load_data()` - Verifies data is loaded correctly from online source
- Data preprocessing: `test_preprocess_data()` - Ensures train/test split works properly
- Model training: `test_train_and_test()` - Validates model training and accuracy
- Prediction: `test_predict()` - Confirms predictions work as expected

**Workflow Steps:**
1. Code passes quality checks and is merged to `dev`
2. Developer creates pull request from `dev` to `test`
3. GitHub Actions automatically runs pytest suite
4. Coverage report is generated and uploaded to Codecov
5. Test summary is stored as an artifact in GitHub Actions
6. PR to `test` branch is only approved if all tests pass
7. Test logs provide detailed feedback on failures if any occur

### 4. Deployment Pipeline

**Implementation:**
- GitHub Actions workflow: `.github/workflows/jenkins_trigger.yml`
- Triggered on: Push and merged pull requests to `master` branch
- Tools: Jenkins, Docker

**Jenkinsfile Stages:**
1. **Checkout**: Retrieves code from the repository
2. **Install Dependencies**: Sets up the Python environment
3. **Run Tests**: Final validation of code quality
4. **Code Quality Check**: Another layer of quality assurance
5. **Build Docker Image**: Containerizes the application
6. **Push to Docker Hub**: Makes image available for deployment
7. **Deploy Application**: Runs the application with admin approval

**Admin Approval Process:**
Jenkins implements an approval gate before deployment:
```groovy
stage('Deploy Application') {
    input {
        message "Deploy to production environment?"
        ok "Yes, deploy it!"
        submitterParameter "APPROVER"
    }
    // Deployment steps
}
```

**Notification System:**
- **Success Email**: Sent when deployment completes successfully
- **Failure Email**: Sent if any pipeline stage fails
- **Slack Notification**: Sent when Jenkins pipeline is triggered

**Workflow Steps:**
1. Code passes all tests and is merged to `master` branch
2. GitHub Actions triggers the Jenkins webhook
3. Jenkins pipeline starts execution
4. Pipeline runs through all stages until it reaches approval gate
5. Admin receives notification that deployment is ready
6. Admin reviews and approves deployment
7. Application is deployed as a Docker container
8. Success/failure notification is sent to stakeholders

## 5. Machine Learning Implementation

The ML project implements a complete workflow:

**Data Loading:**
- Source: UCI Machine Learning Repository (Iris dataset)
- Implementation: `load_data()` in `utils.py`
- Features: Downloads data from URL, applies proper column names

**Data Preprocessing:**
- Implementation: `preprocess_data()` in `utils.py`
- Features: Splits data into train/test sets, handles feature extraction

**Model Implementation:**
- Algorithm: RandomForest classifier
- Implementation: `train()`, `test()`, `predict()` in `model.py`
- Features: Configurable parameters, model persistence, evaluation metrics

**API Endpoints:**
- `GET /`: Home endpoint with version info
- `GET /health`: Health check for monitoring
- `POST /train`: Trains a new model with provided parameters
- `POST /predict`: Makes predictions using the trained model
- `GET /info`: Returns model metadata and configuration

## 📦 Getting Started

### Prerequisites

- Python 3.9+
- Docker
- Jenkins (for full CI/CD pipeline)
- GitHub account

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ml-cicd-project.git
   cd ml-cicd-project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the tests:
   ```bash
   python -m pytest tests/
   ```

5. Run the Flask application locally:
   ```bash
   python src/app.py
   ```

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t iris-ml-app:latest .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 iris-ml-app:latest
   ```

## 🔍 Complete Development Workflow Guide

### Starting a New Feature

1. Update your local repository:
   ```bash
   git checkout dev
   git pull origin dev
   ```

2. Create a feature branch:
   ```bash
   git checkout -b feature/descriptive-name
   ```

3. Make your changes and write tests:
   ```bash
   # Write code in src/
   # Write tests in tests/
   ```

4. Run tests locally to verify:
   ```bash
   python -m pytest tests/
   ```

5. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Descriptive commit message"
   git push origin feature/descriptive-name
   ```

6. Create pull request to `dev` branch on GitHub

### Promoting to Test Environment

1. After PR is approved and merged to `dev`:
   ```bash
   git checkout test
   git pull origin test
   git merge origin/dev
   git push origin test
   ```

2. Create pull request from `test` to `master` on GitHub

3. Monitor GitHub Actions to ensure all tests pass

### Deploying to Production

1. After PR is approved and merged to `master`, Jenkins pipeline will trigger

2. Log in to Jenkins to monitor pipeline execution

3. When prompted, approve the deployment

4. Verify deployment by accessing the application endpoints

## 🔐 Setting Up Secrets

For the CI/CD pipeline to work correctly, you need to set up the following secrets:

1. **GitHub Repository Secrets:**
   - `JENKINS_WEBHOOK_URL`: URL to trigger the Jenkins pipeline
   - `JENKINS_CRUMB`: Jenkins CSRF protection token
   - `SLACK_WEBHOOK_URL`: Slack webhook for notifications

2. **Jenkins Credentials:**
   - `docker-hub-credentials`: Docker Hub username and password

## 🚨 Troubleshooting

### Common GitHub Actions Issues

1. **Flake8 Failures**:
   - Check the specific error code and line number
   - Fix the code quality issue according to Python standards
   - Re-run the workflow

2. **Test Failures**:
   - Examine the test logs for specific failed assertions
   - Check if environment variables are properly set
   - Verify that dependencies are correctly installed

### Jenkins Pipeline Issues

1. **Build Failures**:
   - Check if all required packages are in requirements.txt
   - Verify Docker Hub credentials are correctly configured
   - Check Docker build logs for missing dependencies

2. **Deployment Failures**:
   - Ensure port 5000 is not already in use on the host
   - Verify network connectivity for Docker container
   - Check if Docker Hub rate limits have been reached

## 📊 Project Structure

```
ml-cicd-project/
├── .github/
│   └── workflows/
│       ├── code_quality.yml     # GitHub Action for code quality
│       ├── feature_testing.yml  # GitHub Action for testing
│       └── jenkins_trigger.yml  # GitHub Action to trigger Jenkins
├── src/
│   ├── __init__.py
│   ├── app.py                   # Flask application
│   ├── model.py                 # ML model functions
│   └── utils.py                 # Utility functions
├── tests/
│   ├── __init__.py
│   └── test_app.py              # Unit tests
├── .gitignore
├── Dockerfile                   # Docker configuration
├── Jenkinsfile                  # Jenkins pipeline definition
├── README.md
└── requirements.txt             # Python dependencies
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request to the dev branch