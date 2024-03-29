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

        stage('Install Ansible Role') {
            steps {
                script {
                    sh "ansible-galaxy role install DevRico003.ansible-latest-docker-role"
                }
            }
        }

        stage('Test ') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'SSH_KEY', keyFileVariable: 'SSH_PRIVATE_KEY')]) {
                        sh 'export ANSIBLE_PRIVATE_KEY_FILE=$SSH_PRIVATE_KEY'
                        withCredentials([string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY')]) {
                            sh "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ansible/inventory ansible/test_deploy.yml -e BUILD_ID=${env.BUILD_ID} -e OPENAI_API_KEY=${OPENAI_API_KEY} -e ansible_ssh_private_key_file=$SSH_PRIVATE_KEY"
                        }
                    }
                }
            }
        }
   

        stage('Deploy with Ansible') {
            when {
            // Führen Sie dieses Stage nur aus, wenn das vorherige erfolgreich war
            expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
        }
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'SSH_KEY', keyFileVariable: 'SSH_PRIVATE_KEY')]) {
                        sh 'export ANSIBLE_PRIVATE_KEY_FILE=$SSH_PRIVATE_KEY'
                        withCredentials([string(credentialsId: 'OPENAI_API_KEY', variable: 'OPENAI_API_KEY')]) {
                            sh "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ansible/inventory ansible/prod_deploy.yml -e BUILD_ID=${env.BUILD_ID} -e OPENAI_API_KEY=${OPENAI_API_KEY} -e ansible_ssh_private_key_file=$SSH_PRIVATE_KEY"
                        }
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
