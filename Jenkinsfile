pipeline {
  agent {
    docker {
      image 'qnib/pytest'
      args '-v /home/iko/git/:/test-reports'
    }
    
  }
  stages {
    stage('Build') {
      steps {
        echo 'STAGE: Build'
      }
    }
    stage('Test') {
      steps {
        sh 'pytest --junitxml Graphs/test-reports/results/result.xml Graphs/testing/'
      }
    }
    stage('Report') {
      steps {
        junit 'Graphs/test-reports/results/result.xml'
      }
    }
  }
}