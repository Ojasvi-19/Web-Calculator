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

                        echo "Inside PyInstaller container"
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
                    echo "Starting Calculator app container"
                    docker run -d --name calc-app \
                      -p 5000:5000 \
                      web-calculator:${BUILD_NUMBER}

                    echo "Waiting for app to start..."
                    sleep 10
                    '''

                    docker.image('selenium/standalone-chrome:latest')
                          .inside('--shm-size=2g --network container:calc-app') {
                        sh '''
                        echo "Running Selenium UI Tests"

                        python3 -m pip install --upgrade pip
                        pip install selenium pytest flask

                        ls tests/selenium

                        pytest tests/selenium \
                          --disable-warnings \
                          --maxfail=1
                        '''
                    }

                    sh '''
                    echo "Stopping Calculator app container"
                    docker rm -f calc-app
                    '''
                }
            }
        }

        /* 🔧 FIXED JMETER STAGE (ONLY CHANGE) */
        stage('Run JMeter Performance Tests') {
            steps {
                sh '''
                echo "Running JMeter Performance Tests"

                docker run --rm \
                  -v ${WORKSPACE}/jmeter:/jmeter \
                  justb4/jmeter \
                  sh -c "
                    echo 'Inside JMeter container';
                    ls -l /jmeter;
                    jmeter -n \
                      -t /jmeter/calculator_test.jmx \
                      -l /jmeter/results.jtl
                  "
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



