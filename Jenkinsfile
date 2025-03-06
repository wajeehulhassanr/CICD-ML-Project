pipeline {
    agent any
    
    environment {
        DOCKER_HUB_CREDS = credentials('docker-hub-credentials')
        DOCKER_IMAGE_NAME = 'your-dockerhub-username/iris-ml-app'
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
        EMAIL_RECIPIENTS = 'admin@example.com'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Checked out code from repository"
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
                echo "Installed Python dependencies"
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'python -m pytest tests/ -v'
                echo "All tests passed successfully"
            }
        }
        
        stage('Code Quality Check') {
            steps {
                sh 'flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics'
                echo "Code quality check passed"
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} .
                docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:latest
                """
                echo "Docker image built successfully"
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                sh """
                echo ${DOCKER_HUB_CREDS_PSW} | docker login -u ${DOCKER_HUB_CREDS_USR} --password-stdin
                docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                docker push ${DOCKER_IMAGE_NAME}:latest
                """
                echo "Docker image pushed to Docker Hub"
            }
        }
        
        stage('Deploy Application') {
            input {
                message "Deploy to production environment?"
                ok "Yes, deploy it!"
                submitterParameter "APPROVER"
            }
            
            steps {
                sh """
                # Stop existing container if running
                docker stop iris-ml-app || true
                docker rm iris-ml-app || true
                
                # Run the new container
                docker run -d --name iris-ml-app -p 5000:5000 ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                """
                
                echo "Application deployed successfully by ${APPROVER}"
            }
        }
    }
    
    post {
        success {
            emailext (
                subject: "SUCCESS: Jenkins Pipeline - ${currentBuild.fullDisplayName}",
                body: """
                    <p>The pipeline was successful!</p>
                    <p>Build: ${env.BUILD_NUMBER}</p>
                    <p>Docker Image: ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}</p>
                    <p>Check it out at: <a href='${env.BUILD_URL}'>${env.BUILD_URL}</a></p>
                """,
                to: "${EMAIL_RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
        
        failure {
            emailext (
                subject: "FAILED: Jenkins Pipeline - ${currentBuild.fullDisplayName}",
                body: """
                    <p>The pipeline has failed!</p>
                    <p>Build: ${env.BUILD_NUMBER}</p>
                    <p>Check the logs at: <a href='${env.BUILD_URL}'>${env.BUILD_URL}</a></p>
                """,
                to: "${EMAIL_RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
        
        always {
            cleanWs()
        }
    }
} 