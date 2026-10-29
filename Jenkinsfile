pipeline {
    agent any

    stages {
        stage('Checkout Verified') {
            steps {
                echo 'Source code retrieved from GitHub.'
            }
        }

        stage('Verify Python') {
            steps {
                bat 'python --version'
                bat 'python -m pip --version'
            }
        }

        stage('Verify Docker') {
            steps {
                bat 'docker version'
                bat 'docker ps'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Unit and API Tests') {
            steps {
                bat 'python -m pytest tests/unit tests/api -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t medvision-ci:jenkins .'
            }
        }
    }

    post {
        success {
            echo 'MedVision-CI: automated tests and Docker build passed!'
        }
        failure {
            echo 'MedVision-CI: pipeline failed. Check the console output.'
        }
    }
}