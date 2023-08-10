pipeline {
    agent any

    tools {nodejs "Nodejs"}

    stages {
        stage("Testing Api...") {
            stages{
                stage("Set up python enviroment for testing"){
                    agent {
                        docker {
                            image 'python:3.11.4-bookworm'
                            args '-u root --privileged'
                        }
                    }
                    steps{
                        
                        script {
                            sh 'pip install --user virtualenv'
                            sh 'python3 -m venv .venv'
                            sh '. .venv/bin/activate'
                            sh 'pip install -r requiremen ts.txt'
                            def commandOutput = sh returnStdout: true, script: 'python main.py', 
                            if(commandOutput.contains('INFO:     Application startup complete.')){
                                echo "main.py 运行成功！"
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
