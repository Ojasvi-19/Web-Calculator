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
                  --ignore=tests/selenium \
                  --cov=Calculator_ops \
                  --cov-report=term \
                  --cov-report=xml
                '''
            }
        }

        stage('Run Selenium UI Tests') {
            steps {
                script {
                    sh '''
                    docker run -d --name calc-app \
                      -p 5000:5000 \
                      web-calculator:${BUILD_NUMBER}

                    sleep 10
                    '''

                    docker.image('selenium/standalone-chrome:latest')
                          .inside('--shm-size=2g --network container:calc-app') {
                        sh '''
                        pip install selenium pytest flask
                        pytest tests/selenium --maxfail=1
                        '''
                    }
                }
            }
        }

        /* ✅ FIXED JMeter STAGE — NOTHING ELSE TOUCHED */
        stage('Run JMeter Performance Tests') {
            steps {
                sh '''
                echo "Running JMeter Performance Tests"

                echo "Checking JMeter files:"
                ls -l ${WORKSPACE}/jmeter

                docker run --rm \
                  --network container:calc-app \
                  -v ${WORKSPACE}/jmeter:/jmeter \
                  justb4/jmeter:latest \
                  -n \
                  -t /jmeter/calculator_test.jmx \
                  -l /jmeter/results.jtl
                '''
            }
        }

        stage('Stop Calculator App') {
            steps {
                sh 'docker rm -f calc-app || true'
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




