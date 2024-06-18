pipeline {
    agent {
        docker {
            image 'your-docker-registry/jenkins-python:latest'
            args '-v /root/libs/ImpalaJDBC42.jar:/root/libs/ImpalaJDBC42.jar'
        }
    }

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
                // Run the Python script
                sh '''
                source ${PYTHON_ENV}/bin/activate
                python main.py
                '''
            }
        }
    }
}
