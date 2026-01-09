pipeline {
    agent any

    triggers {
        // 每2分钟轮询一次
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                # 创建结果目录
                mkdir -p allure-results
                # 运行测试并生成Allure结果
                pytest ./ --alluredir=allure-results || true
                '''
            }
        }

        stage('Generate Report') {
            steps {
                sh '''
                # 安装Allure命令行工具（如果没安装）
                if ! command -v allure &> /dev/null; then
                    echo "安装Allure..."
                    # 使用wget下载（或者你可以提前在Jenkins中配置）
                    wget https://github.com/allure-framework/allure2/releases/download/2.20.1/allure-2.20.1.tgz
                    tar -zxvf allure-2.20.1.tgz
                    export PATH=$PATH:$PWD/allure-2.20.1/bin
                fi

                # 生成HTML报告
                allure generate allure-results -o allure-report --clean
                '''
            }
            post {
                always {
                    // 发布Allure报告
                    allure([
                        includeProperties: false,
                        jdk: '',
                        results: [[path: 'allure-results']],
                        reportBuildPolicy: 'ALWAYS'
                    ])
                }
            }
        }

        stage('Send Email') {
            steps {
                script {
                    // 发送邮件（最简单的方式）
                    mail to: '625875899@qq.com',
                         subject: "Jenkins构建结果: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                         body: """
                         构建完成！

                         项目: ${env.JOB_NAME}
                         构建号: ${env.BUILD_NUMBER}
                         状态: ${currentBuild.result ?: 'SUCCESS'}

                         查看报告: ${env.BUILD_URL}allure/
                         控制台输出: ${env.BUILD_URL}console
                         """
                }
            }
        }
    }

    post {
        always {
            // 清理工作空间
            deleteDir()
        }
    }
}