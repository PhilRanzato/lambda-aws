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
            sh 'zip function.zip lambda.py'
          }
      }
      stage('Checkout Terraform') {
          steps {
            sh 'git clone https://github.com/PhilRanzato/terraform-lambda-aws'
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
