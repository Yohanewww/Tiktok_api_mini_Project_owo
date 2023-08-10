pipeline {
    agent any

    tools {nodejs "Nodejs"}

    stages {
        stage("Testing Api...") {
            stages{
                stage("Set up python enviroment for testing"){
                    agent none
                    steps{
                        sh 'pip install --user virtualenv'
                        sh 'python3 -m venv .venv'
                        sh '. .venv/bin/activate'
                        sh 'pip install -r requirements.txt'
                        sh 'lsof -ti :8000 | xargs kill -9 || true'// 杀掉之前的进程
                        sh 'python3 main.py'
                    }
                }
                

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

                stage('Post-processing') {
                    steps {
                        script {
                            // 停止和删除 Python 环境
                            sh 'deactivate || true'
                            sh 'rm -rf venv || true'
                        }
                    }
                }
            }
        }
        // stage('Build') {
        //     steps {
        //         // 构建 Docker 镜像
        //         sh 'docker build -t projectowo .'
        //     }
        // }

        // stage('Deploy') {
        //     steps {
        //         // 部署 Docker 容器
        //         sh 'docker run -d -p 3366:8000 projectowo'
        //     }
        // }
    }
}
