pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Ojasvi-19/Web-Calculator.git'
            }
        }

        stage('Verify Workspace') {
            steps {
                sh '''
                echo "Workspace:"
                pwd
                ls -l
                '''
            }
        }

        stage('Build Executable with PyInstaller') {
            steps {
                script {
                    docker.image('python:3.10-slim').inside {
                        sh '''
                        set -e

                        echo "Inside container:"
                        pwd
                        ls -l

                        if [ ! -f Calculator.py ]; then
                          echo "Calculator.py NOT FOUND"
                          exit 1
                        fi

                        apt-get update
                        apt-get install -y binutils
                        pip install --no-cache-dir -r Requirements.txt
                        pip install --no-cache-dir pyinstaller

                        pyinstaller --onefile Calculator.py
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t web-calculator:${BUILD_NUMBER} .'
            }
        }

        stage('Run Unit Tests & Coverage') {
            steps {
                sh '''
                docker run --rm \
                  web-calculator:${BUILD_NUMBER} \
                  pytest tests \
                  --cov=Calculator_ops \
                  --cov-report=term \
                  --cov-report=xml
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                script {
                    docker.image('python:3.10-slim').inside {
                        sh '''
                        set -e
                        apt-get update
                        apt-get install -y chromium chromium-driver

                        pip install -r Requirements.txt
                        pip install selenium pytest

                        cd Web-Calculator

                        python Calculator.py &
                        sleep 5

                        pytest tests/selenium --disable-warnings --maxfail=1
                        '''
                    }
                }
            }
        }

        stage('Run JMeter Performance Tests') {
            steps {
                sh '''
                docker run --rm \
                  -v "$PWD/jmeter:/jmeter" \
                  justb4/jmeter \
                  -n \
                  -t /jmeter/calculator_test.jmx \
                  -l /jmeter/results.jtl
                '''
            }
        }

        stage('Archive Executable') {
            steps {
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "Pipeline executed successfully"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}







