
pipeline {
    agent any

    stages {
        stage('Checkout Verified') {
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

        stage('Run Selenium UI Tests') {
            steps {
                bat 'docker rm -f medvision-selenium-jenkins 2>NUL || exit /b 0'

                bat 'docker run -d --name medvision-selenium-jenkins -p 4444:4444 --shm-size="2g" selenium/standalone-chrome:latest'

                powershell '''
                    $deadline = (Get-Date).AddMinutes(2)

                    do {
                        try {
                            $response = Invoke-RestMethod `
                                -Uri "http://localhost:4444/status" `
                                -TimeoutSec 5

                            if ($response.value.ready -eq $true) {
                                Write-Host "Selenium Chrome is ready."
                                exit 0
                            }
                        } catch {
                            Write-Host "Waiting for Selenium Chrome..."
                        }

                        Start-Sleep -Seconds 3
                    } while ((Get-Date) -lt $deadline)

                    throw "Selenium Chrome did not become ready."
                '''

                bat 'python -m pytest tests/selenium -v'
            }
            post {
                always {
                    bat 'docker rm -f medvision-selenium-jenkins 2>NUL || exit /b 0'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t medvision-ci:jenkins .'
            }
        }

        stage('Container Health Check') {
            steps {
                bat 'docker rm -f medvision-ci-test 2>NUL || exit /b 0'
                bat 'docker run -d --name medvision-ci-test -p 5001:5000 medvision-ci:jenkins'
                bat 'python health_check.py'
            }
            post {
                always {
                    bat 'docker rm -f medvision-ci-test 2>NUL || exit /b 0'
                }
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
        always {
            bat 'docker rm -f medvision-selenium-jenkins 2>NUL || exit /b 0'
            bat 'docker rm -f medvision-ci-test 2>NUL || exit /b 0'
        }
    }
}
