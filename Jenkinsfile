pipeline {
    agent any

    environment {
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
        KUBECTL = '/usr/local/bin/kubectl'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r app/requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    ./venv/bin/pytest -v
                '''
            }
        }

        stage('Build Container Image') {
            steps {
                sh '''
                    podman build -t cloud-native-devops:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    ${KUBECTL} apply -f kubernetes/deployment.yaml
                    ${KUBECTL} apply -f kubernetes/service.yaml
                '''
            }
        }

        stage('Verify Kubernetes Deployment') {
            steps {
                sh '''
                    ${KUBECTL} rollout status deployment/cloud-native-devops
                    ${KUBECTL} get pods
                    ${KUBECTL} get services
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'CI/CD pipeline failed. Check the stage logs.'
        }
    }
}
