pipeline {
    agent any

    environment {
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
        KUBECTL = '/usr/local/bin/kubectl'
        DOCKERHUB_USERNAME = 'hgreen1077'
        IMAGE_NAME = "hgreen1077/cloud-native-devops"
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
                    podman build \
                      -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                      -t ${IMAGE_NAME}:latest \
                      .
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'REGISTRY_USERNAME',
                        passwordVariable: 'REGISTRY_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        echo "${REGISTRY_TOKEN}" | podman login docker.io \
                            --username "${REGISTRY_USERNAME}" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                sh '''
                    podman push ${IMAGE_NAME}:${BUILD_NUMBER}
                    podman push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Logout from Docker Hub') {
            steps {
                sh '''
                    podman logout docker.io || true
                '''
            }
        }
    }

    post {
        success {
            echo 'CI pipeline and Docker Hub image push completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs.'
        }
    }
}
