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
                sh '''
                    set -e

                    echo "Python version:"
                    python3 --version

                    echo "Ensuring pip..."
                    python3 -m ensurepip --upgrade

                    echo "Upgrading pip..."
                    python3 -m pip install --upgrade pip

                    echo "Installing PyInstaller..."
                    python3 -m pip install --user pyinstaller

                    echo "Verifying Calculator.py..."
                    ls -l Calculator.py

                    echo "Building executable..."
                    ~/.local/bin/pyinstaller --onefile Calculator.py

                    echo "Build complete. dist contents:"
                    ls -l dist
                    '''
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

        stage('Archive Executable') {
            steps {
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }
    }
}











