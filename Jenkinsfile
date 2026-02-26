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

        stage('Run Selenium UI Tests') {
            steps {
                script {
                    sh '''
                    echo "Starting Calculator app container"
                    docker run -d --name calc-app -p 5000:5000 web-calculator:${BUILD_NUMBER}

                    sleep 5

                    echo "Running Selenium Tests"
                    docker run --rm \
                      --network host \
                      -v "$PWD/tests:/tests" \
                      python:3.10-slim \
                      bash -c "
                        pip install selenium pytest webdriver-manager &&
                        pytest /tests/selenium
                      "

                    echo "Stopping Calculator app container"
                    docker rm -f calc-app
                    '''
                }
            }
        }

        stage('Run JMeter Performance Tests') {
            steps {
                sh '''
                echo "Checking JMeter files"
                ls -l jmeter || true

                if [ ! -f jmeter/calculator_test.jmx ]; then
                    echo "ERROR: jmeter/calculator_test.jmx NOT FOUND"
                    exit 1
                fi

                echo "Running JMeter Performance Tests"

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



