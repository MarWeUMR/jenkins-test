pipeline {
    agent any
    environment {
        // Define environment variables if needed
        PYTHON_ENV = '/usr/bin/python3'
        VENV_DIR = 'venv'
        NO_COLOR= "true"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from your repository
                git branch: 'main', url: 'https://github.com/MarWeUMR/jenkins-test.git'
            }
        }

        stage('Setup Environment') {
            steps {
                // Create and activate virtual environment, then install dependencies
                sh '''
                # Create virtual environment
                python3 -m venv ${VENV_DIR}

                # Activate virtual environment
                . ${VENV_DIR}/bin/activate

                # Install required Python packages
                pip install jaydebeapi pandas structlog
                '''
            }
        }

        stage('Run Script') {
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'cldr', usernameVariable: 'IMPALA_USER', passwordVariable: 'IMPALA_PASSWORD')
                ]) {
                    // Run the Python script
                    sh '''
                      . ${VENV_DIR}/bin/activate
                      python main.py
                    '''
                }
            }
        }
        stage('Archive Artifacts') {
            steps {
                // Archive the generated CSV file
                archiveArtifacts artifacts: 'output/*.csv', fingerprint: true
            }
        }
    }
    post {
            always {
                // Clean up actions, if any
                cleanWs()
            }
    }
}
