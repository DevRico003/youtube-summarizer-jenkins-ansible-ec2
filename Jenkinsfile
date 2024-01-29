pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials-id'
        IMAGE_NAME = 'devrico003/youtube-summarizer-new'
    }

    stages {
        stage('Clone repository') {
            steps {
                echo 'Start: Cloning repository...'
                checkout scm: [
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    userRemoteConfigs: [[
                        credentialsId: 'github-id', 
                        url: 'https://github.com/DevRico003/jenkins-ansible-ec2.git'
                    ]]
                ]
                echo 'End: Repository cloned.'
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    def dockerImage = docker.build("${IMAGE_NAME}:${env.BUILD_ID}", ".")
                    dockerImage.tag('latest')
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_CREDENTIALS_ID) {
                        def dockerImage = docker.image("${IMAGE_NAME}:${env.BUILD_ID}")
                        dockerImage.push()
                        dockerImage.tag('latest')
                        dockerImage.push('latest')
                    }
                }
            } 
        }

        stage('Deploy on Jenkins Host') {
            steps {
                script {
                    // Stoppen und Entfernen eines möglicherweise vorhandenen alten Containers
                    sh "docker stop youtube-summarizer || true"
                    sh "docker rm youtube-summarizer || true"
                    // Deploying unter Verwendung des OpenAI API-Keys
                    withCredentials([string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY')]) {
                        // Starten des neuen Containers mit der Umgebungsvariable
                        sh "docker run -d --name youtube-summarizer -p 8501:8501 -e OPENAI_API_KEY=${OPENAI_API_KEY} ${IMAGE_NAME}:${env.BUILD_ID}"
                    }
                }
            }
       }
    } 

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
    }
}
