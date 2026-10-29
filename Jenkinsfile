
pipeline {
    agent any

    stages {
        stage('Checkout Verified') {
            steps {
                echo 'MedVision-CI source code has been retrieved from GitHub.'
            }
        }

        stage('Verify Python') {
            steps {
                bat 'python --version'
            }
        }

        stage('Project Structure') {
            steps {
                bat 'dir'
            }
        }
    }

    post {
        success {
            echo 'MedVision-CI pipeline completed successfully!'
        }
        failure {
            echo 'MedVision-CI pipeline failed. Check the console output.'
        }
    }
}
