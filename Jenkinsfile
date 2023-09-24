pipeline {
  agent { label 'docker' }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub_jenkins')
  }
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t 18066791/flask-app:latest .'
      }
    }
    stage('Login') {
      steps {
        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
      }
    }
    stage('Push') {
      steps {
        sh 'docker push 18066791/flask-app:latest'
      }
    }
  }
  post {
    always {
      sh 'docker logout'
    }
  }
}
