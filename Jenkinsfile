groovy
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
                sh '''
                echo "安装依赖..."
                # 如果有requirements.txt
                if [ -f "requirements.txt" ]; then
                    pip install -r requirements.txt
                fi
                # 安装必要的包
                pip install pytest allure-pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                echo "运行测试..."
                # 创建结果目录
                mkdir -p allure-results

                # 方法1：直接运行pytest
                # pytest . --alluredir=allure-results -v || true

                # 方法2：运行你的Python脚本
                python run_tests.py || true

                # 检查是否生成了数据
                echo "检查生成的数据..."
                if [ -d "allure-results" ]; then
                    echo "生成的文件:"
                    ls -la allure-results/
                    echo "文件数量: $(ls -1 allure-results | wc -l)"
                fi
                '''
            }
        }

        stage('Generate Report') {
            steps {
                sh '''
                echo "生成Allure报告..."
                # 检查是否有数据
                if [ ! -d "allure-results" ] || [ -z "$(ls -A allure-results)" ]; then
                    echo "错误：没有找到Allure结果文件"
                    exit 1
                fi
                '''
            }
            post {
                always {
                    // 使用Jenkins的Allure插件生成报告
                    allure([
                        includeProperties: false,
                        jdk: '',
                        results: [[path: 'allure-results']],
                        reportBuildPolicy: 'ALWAYS',
                        // 可选：指定报告版本
                        // report: '2.20.1'
                    ])
                }
            }
        }

        stage('Send Email') {
            steps {
                script {
                    // 构建结果
                    def buildResult = currentBuild.result ?: 'SUCCESS'
                    def allureUrl = "${env.BUILD_URL}allure/"

                    // 读取测试结果统计
                    def testCount = 0
                    def passedCount = 0
                    def failedCount = 0

                    try {
                        sh '''
                        # 统计测试结果
                        if [ -d "allure-results" ]; then
                            echo "统计测试结果..."
                            # 这里可以添加统计逻辑
                        fi
                        '''
                    } catch (Exception e) {
                        echo "统计测试结果失败: ${e}"
                    }

                    mail to: '625875899@qq.com',
                         subject: "Jenkins构建结果: ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${buildResult}",
                         body: """
                         构建完成！

                         项目: ${env.JOB_NAME}
                         构建号: ${env.BUILD_NUMBER}
                         构建状态: ${buildResult}
                         构建地址: ${env.BUILD_URL}

                         📊 测试报告: ${allureUrl}
                         📝 控制台输出: ${env.BUILD_URL}console

                         测试结果:
                         - 总测试数: ${testCount}
                         - 通过: ${passedCount}
                         - 失败: ${failedCount}

                         详细报告请查看: ${allureUrl}
                         """
                }
            }
        }
    }

    post {
        always {
            // 清理工作空间（可选）
            // deleteDir()

            // 或者只清理部分文件
            sh '''
            echo "清理临时文件..."
            # 保留报告，只清理其他文件
            rm -rf __pycache__/
            rm -rf .pytest_cache/
            '''

            // 归档重要文件
            archiveArtifacts artifacts: 'allure-report/**', fingerprint: true
        }

        success {
            echo '构建成功！'
        }

        failure {
            echo '构建失败！'
            // 可以在这里添加失败通知
        }
    }
}