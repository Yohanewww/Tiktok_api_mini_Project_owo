pipeline {
    agent any

    tools {nodejs "{Nodejs}"}

    stages {
        stage('Install Apifox CLI') {
            steps {
                sh 'npm install -g apifox-cli'
            }
        }

        stage('Running Test Scenario') {
            steps {
                sh 'apifox run https://api.apifox.cn/api/v1/projects/3122443/api-test/ci-config/371736/detail?token=xprxMUsWMeDnlbJheRIxvx -r html,cli'
            }
        }
        stage('Build') {
            steps {
                // 构建 Docker 镜像
                sh 'docker build -t projectowo .'
            }
        }

        stage('Deploy') {
            steps {
                // 部署 Docker 容器
                sh 'docker run -d -p 3366:8000 projectowo'
            }
        }
    }
}
