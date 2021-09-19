pipeline {
  agent {
    node {
      label 'c7vfc'
    }
  }
  environment {
    terraform_varsfile = 'testing.tfvars'
  }
  stages { 
      stage('Build Lambda') {
          steps {
            sh 'ls'
              echo 'Building Lambda'
        }
      }
      stage('CodeQuality Lambda') {
          steps {
              echo 'Code Quality Scanning'
        }
      }
      stage('Zip Lambda') {
          steps {
            sh 'ls'
            sh 'zip function.zip lambda.py'
            sh 'ls'
          }
      }
      stage('Checkout Terraform') {
          steps {
//             checkout([$class: 'GitSCM', branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'dd3d6b99-7083-4204-8d57-e0282ace0473', url: 'https://github.com/PhilRanzato/terraform-lambda-aws']]])
            sh 'git clone https://github.com/PhilRanzato/terraform-lambda-aws'
            sh 'ls'
          }
      }
      stage('Terraform deploy') {
          steps {
              sh 'mv function.zip terraform-lambda-aws/'
              withCredentials([string(credentialsId: 'TF_VAR_secret_key', variable: 'TF_VAR_secret_key'), string(credentialsId: 'TF_VAR_access_key', variable: 'TF_VAR_access_key')]) {
                sh '''
                  cd terraform-lambda-aws
                  terraform init
                  terraform validate
                  terraform plan -var-file=$terraform_varsfile
                  terraform apply -var-file=$terraform_varsfile --auto-approve
                '''
              }
          }
      }
    }
    post {
        always {
            cleanWs(deleteDirs: true)
        }
    }
}
