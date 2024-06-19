pipeline {
    agent any
    environment {
        // Define environment variables if needed
        PYTHON_ENV = '/usr/bin/python3'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from your repository
                git 'https://github.com/MarWeUMR/jenkins-test.git'
            }
        }
        stage('Setup Environment') {
            steps {
                // Install dependencies, if any
                sh '''
                # Activate virtual environment
                source ${PYTHON_ENV}/bin/activate

                # Install required Python packages
                pip install jaydebeapi pandas
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
                source ${PYTHON_ENV}/bin/activate
                python main.py
                '''
                }
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
