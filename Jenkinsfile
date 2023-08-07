Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // 检出代码库
                git 'https://github.com/yohaneowo/Tiktok_api_mini_Project_owo.git'
            }
        }

        stage('Build') {
            steps {
                // 构建 Docker 镜像
                sh 'docker build -t my-fastapi-app .'
            }
        }

        // stage('Test') {
        //     steps {
        //         // 运行测试
        //         sh 'docker run my-fastapi-app pytest'
        //     }
        // }

        // stage('Deploy') {
        //     steps {
        //         // 部署 Docker 容器
        //         sh 'docker run -d -p 8000:8000 my-fastapi-app'
        //     }
        // }
    }
}
