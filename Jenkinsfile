pipeline {
    agent any
    stages {

        stage('Build') {
            steps {
                // 构建 Docker 镜像
                sh 'docker build projectowo .'
            }
        }

        stage('Deploy') {
            steps {
                // 部署 Docker 容器
                sh 'docker run -d -p 8000:8000 projectowo'
            }
        }
    }
}
