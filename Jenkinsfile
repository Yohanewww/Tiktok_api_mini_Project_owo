pipeline {
    agent any
    stages {

        stage('Build') {
            steps {
                // 构建 Docker 镜像
                sh 'docker build -t my-fastapi-app .'
            }
        }

        stage('Test') {
            steps {
                // 运行测试
                sh 'docker run my-fastapi-app pytest'
            }
        }

        stage('Deploy') {
            steps {
                // 部署 Docker 容器
                sh 'docker run -d -p 8000:8000 my-fastapi-app'
            }
        }
    }
}
