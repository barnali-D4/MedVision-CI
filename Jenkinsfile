
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
    }

    post {
        success {
            echo 'MedVision-CI: automated tests passed!'
        }
        failure {
            echo 'MedVision-CI: pipeline failed. Check the console output.'
        }
    }
}
