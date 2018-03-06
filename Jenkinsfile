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
      post {
        always {
          junit 'Graphs/test-reports/results/result.xml'
          
        }
      }
    }
  }
  post {
    failure {
      mail(to: 'ikobh7@gmail.com', subject: "Failed Pipeline: ${currentBuild.fullDisplayName}", body: "Something is wrong with ${env.BUILD_URL}")
      
    }
    
  }

  triggers {
    cron('0 22 * * *')
  }
}
