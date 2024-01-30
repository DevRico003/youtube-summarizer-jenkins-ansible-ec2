pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials-id' 
    }

    stages {
        stage('Clone repository') {
            steps {
                echo 'Start: Cloning repository...'
                checkout scm: [$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[credentialsId: 'github-id', url: 'https://github.com/DevRico003/jenkins-ansible-ec2.git']]]
                echo 'End: Repository cloned.'
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    echo "Building Docker image with tag: ${env.BUILD_ID}"
                    sh "docker build -t devrico003/youtube-summarizer-small:${env.BUILD_ID} ."
                    echo "Tagging image with 'latest'"
                    sh "docker tag devrico003/youtube-summarizer-small:${env.BUILD_ID} devrico003/youtube-summarizer-small:latest"
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    echo 'Logging into DockerHub...'
                    withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                        sh "echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin"
                    }
                    echo "Pushing Docker image with tag: ${env.BUILD_ID}"
                    sh "docker push devrico003/youtube-summarizer-small:${env.BUILD_ID}"
                    echo "Pushing Docker image with tag: latest"
                    sh "docker push devrico003/youtube-summarizer-small:latest"
                }
            } 
        }

        stage('Deploy on Jenkins Host') {
            steps {
                script {
                    echo "Deploying on Jenkins Host as Docker container with image tag: ${env.BUILD_ID}"
                    // Stoppen und Entfernen eines möglicherweise vorhandenen alten Containers
                    sh "docker stop youtube-summarizer || true"
                    sh "docker rm youtube-summarizer || true"
                    // Deploying unter Verwendung des OpenAI API-Keys
                    withCredentials([string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY')]) {
                        // Starten des neuen Containers mit der Umgebungsvariable
                        sh "docker run -d --name youtube-summarizer -p 8501:8501 -e OPENAI_API_KEY=${OPENAI_API_KEY} devrico003/youtube-summarizer-small:${env.BUILD_ID}"
                    }
                }
            }
       }
    } 


    // post {
    //     always {
    //         echo 'Cleaning up workspace...'
    //         cleanWs()
    //     }
    // }
}
