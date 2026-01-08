pipeline {
    agent any // 1. 指定在哪执行：在任何可用的Jenkins代理上运行
    stages { // 2. 定义阶段：整个流程分为以下几个大步骤
        stage('Checkout') { // 阶段1：拉取代码
            steps {
                git branch: 'main', url: 'https://github.com/QQYB-nn/PYTEST.git'
            }
        }
        stage('Install Dependencies') { // 阶段2：安装依赖
            steps {
                sh 'pip install -r requirements.txt' // 执行shell命令
            }
        }
        stage('Run Tests') { // 阶段3：运行测试
            steps {
                sh 'pytest --alluredir=./allure-results' // 运行测试并生成Allure数据
            }
        }
    }
    post { // 3. 后置操作：无论成功失败，最后都会执行的步骤
        always {
            allure includeProperties: false,
                  jdk: '',
                  results: [[path: 'allure-results']] // 发布Allure报告
        }
    }
}