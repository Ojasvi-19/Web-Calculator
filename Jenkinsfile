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
                echo "Workspace path:"
                pwd
                echo "Workspace contents:"
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

                echo "Ensuring pip is installed..."
                python3 -m ensurepip --upgrade

                echo "Upgrading pip..."
                python3 -m pip install --upgrade pip

                echo "Installing PyInstaller..."
                python3 -m pip install --user pyinstaller

                echo "Checking Calculator.py..."
                ls -l Calculator.py

                echo "Building executable..."
                ~/.local/bin/pyinstaller --onefile Calculator.py

                echo "dist directory:"
                ls -l dist
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
            echo 'Pipeline executed successfully'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}












