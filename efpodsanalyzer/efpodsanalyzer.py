# !/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import json
import os
import re
import sys
# import webbrowser
import shutil

# 错误码
ERROR_PARAMETERS_COUNT = 1  # 参数数量错误
ERROR_PARAMETERS_TYPE = 2   # 参数错误
ERROR_NEED_PODS = 3         # Pods 目录不存在或不完整
ERROR_FILE_CORRUPTED = 4    # 文件损坏或格式不正确
ERROR_FILE_NOT_EXIST = 5    # 文件不存在

# 文件名长度
SELF_FILENAME_LEN = len(sys.argv[0].split('/')[-1])
POD_FILENAME_LEN = len(sys.argv[1].split('/')[-1])

# 路径相关
PROJECT_NAME = "efpodsanalyzer"
MODULE_NAME = PROJECT_NAME.lower()
ROOT_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR = os.path.join(ROOT_PROJECT_DIR, MODULE_NAME)

# 原始数据单元
class ManifestPodClass:
    'Manifest中取出的未处理数据单元'
    podName = ''
    podDependencies = []

    def __init__(self, name, dependencies):
        self.podName = name
        self.podDependencies = dependencies

    def dependenciesCount(self):
        return len(self.podDependencies)

    @staticmethod
    def printList(Objectlist):
        for object in Objectlist:
            print(object.podName, object.podDependencies)

# 最终数据单元
class PodClass:
    '处理后的数据单元'
    podName = ''
    podDependencyIndexes = []
    podReferenceCount = 1

    def __init__(self, name, dependencyIndexes):
        self.podName = name
        self.podDependencyIndexes = dependencyIndexes

    def dependenciesCount(self):
        return len(self.podDependencyIndexes)

    def dependencies(self, podList):
        return [podList[i] for i in self.podDependencyIndexes]

    @staticmethod
    def printList(Objectlist):
        for object in Objectlist:
            print(object.podName, object.podDependencyIndexes)

# 从 Manifest.lock 读取 PODS 原始数据单元列表
def readManifestPodListFromFile(fileName):
    fo = open(fileName, "r+")
    manifestFileContent = fo.read()
    fo.close()
    spliteList = manifestFileContent.split('DEPENDENCIES:')
    if len(spliteList) <= 1:
        print('Error: The Manifest.lock file is corrupted!')
        exit(ERROR_FILE_CORRUPTED)
    podsString = '  ' + spliteList[0][5:].strip(' \n')
    podsStringList = podsString.split('\n')
    # 生成原始数据单元数组
    returnList = []
    index = -1
    lastObject = ManifestPodClass('', [])
    for line in podsStringList:
        lineClean = line.replace('\'','').replace('\"','')
        podName = lineClean.lstrip(' -').split(' ')[0]
        if lineClean.startswith('    - '):
            if index >= 0:
                lastObject.podDependencies.append(podName)
        elif lineClean.startswith('  - '):
            if index >= 0:
                returnList.append(lastObject)
            index = index + 1
            lastObject = ManifestPodClass(podName, [])
        else:
            print('Error: The Manifest.lock file is corrupted!')
            exit(ERROR_FILE_CORRUPTED)
    returnList.append(lastObject)
    return returnList

# 从 ManifestPodList 生成最终数据单元列表
def generatePodListFromList(manifestPodList):
    def getBaseIndexes(dependencies, baseList):
        returnList = []
        if 0 == len(dependencies):
            return returnList
        for dependency in dependencies:
            tempMark = False
            for index, base in enumerate(baseList):
                if base.podName == dependency:
                    returnList.append(index)
                    tempMark = True
            if False == tempMark:
                return returnList
        return returnList

    returnList = []
    nextList = list(manifestPodList)
    while 0 < len(nextList):
        doingList = list(nextList)
        for manifestPod in doingList:
            baseIndexes = getBaseIndexes(manifestPod.podDependencies, returnList)
            if len(baseIndexes) == len(manifestPod.podDependencies):
                returnList.append(PodClass(manifestPod.podName, baseIndexes))
                nextList.remove(manifestPod)
                # 权重
                for baseIndex in baseIndexes:
                    returnList[baseIndex].podReferenceCount += 1
                    # print(str(baseIndex) + "+= 1, podReferenceCount = " + str(returnList[baseIndex].podReferenceCount))
    return returnList

# 生成依赖关系图
def generateDependencyGraph(podlist, configString):
    # Directory
    directory = podFilePath() + "EFPADiagram"
    if not os.path.exists(directory):
        os.makedirs(directory)

    configObject = json.loads(configString)

    settingTitle = podFileDirectoryName()
    settingCategories = json.dumps(configObject['config']['categories'])
    settingCategoryRegexes = configObject['config']['categoryRegexes']
    settingContent = "setting = '{\"setting\": {\"title\": \"" + \
        settingTitle + "\",\"categories\": " + str(settingCategories) + "}}';"
    xx = open(podFilePath() + "EFPADiagram/setting.json", "w+")
    xx.write(settingContent)
    xx.close()

    # Data
    nodeString = ""
    for index, pod in enumerate(podlist):
        podValue = str(pod.podReferenceCount)
        podID = str(index)
        podLabel = pod.podName
        podAttvalue = str(1)
        for index, regex in enumerate(settingCategoryRegexes):
            if re.match(regex, pod.podName):
                # print(pod.podName + " -> " + regex)
                podAttvalue = str(index)
                break

        nodeString = nodeString + "{\"attvalues\": {\"attvalue\": {\"_for\": \"modularity_class\",\"_value\": \"" + podAttvalue + \
            "\"}},\"size\": {\"_value\": \"" + podValue + "\",\"__prefix\": \"viz\"},\"position\": {\"_x\": \"-225.73984\",\"_" + \
            "y\": \"82.41631\",\"_z\": \"0.0\",\"__prefix\": \"viz\"},\"color\": {\"_r\": \"236\",\"_g\": \"81\",\"_b\": \"72\"" + \
            ",\"__prefix\": \"viz\"},\"_id\": \"" + podID + "\",\"_label\": \"" + podLabel + "\"}"
        nodeString = nodeString + ","

    if nodeString.endswith(","):
        nodeString = nodeString[:-1]

    edgeString = ""
    edgeIndex = 0
    for index, pod in enumerate(podlist):
        if pod.dependenciesCount() > 0:
            for podDependencyIndex in pod.podDependencyIndexes:
                podID = str(edgeIndex)
                podSource = str(index)
                podTarget = str(podDependencyIndex)
                edgeIndex += 1
                edgeString = edgeString + "{\"attvalues\": \"\",\"_id\": \"" + podID + "\",\"_source\": \"" + \
                    podSource + "\",\"_target\": \"" + podTarget + "\",\"_weight\": \"16.0\"}"
                edgeString = edgeString + ","

    if edgeString.endswith(","):
        edgeString = edgeString[:-1]

    oo = open(resourcePath("template/data.json"), "r+")
    dataTemplate = oo.read()
    oo.close()

    dataContent = "data = \'" + dataTemplate.replace("$nodes$", nodeString).replace("$edges$", edgeString).replace("\n", "") + "\';"
    xx = open(podFilePath() + "EFPADiagram/data.json", "w+")
    xx.write(dataContent)
    xx.close()

    # JS
    directoryJS = podFilePath() + "EFPADiagram/js"
    if not os.path.exists(directoryJS):
        os.makedirs(directoryJS)
    shutil.copy(resourcePath("EFPADiagram/js/dataTool.js"), directoryJS + "/dataTool.js")
    shutil.copy(resourcePath("EFPADiagram/js/echarts.min.js"), directoryJS + "/echarts.min.js")
    shutil.copy(resourcePath("EFPADiagram/js/jquery.min.js"), directoryJS + "/jquery.min.js")
    shutil.copy(resourcePath("EFPADiagram/js/xml2json.min.js"), directoryJS + "/xml2json.min.js")

    # CSS
    directoryCSS = podFilePath() + "EFPADiagram/css"
    if not os.path.exists(directoryCSS):
        os.makedirs(directoryCSS)
    shutil.copy(resourcePath("EFPADiagram/css/style.css"), directoryCSS + "/style.css")

    # HTML
    graphHtmlPath = podFilePath() + "EFPADiagram/"
    shutil.copy(resourcePath("EFPADiagram/graph_circular.html"), graphHtmlPath + "graph_circular.html")
    shutil.copy(resourcePath("EFPADiagram/graph_force.html"), graphHtmlPath + "graph_force.html")
    shutil.copy(resourcePath("EFPADiagram/index.html"), graphHtmlPath + "index.html")
    print("Dependency graph generated: " + graphHtmlPath)

    # webbrowser.open("file://" + graphHtmlPath)

    return

# 生成资源文件目录访问路径
def resourcePath(relativePath):
    return os.path.join(MODULE_DIR, relativePath)

# 当前文件所在路径
def selfFilePath():
    return sys.argv[0][:-SELF_FILENAME_LEN]

# 目标文件所在路径
def podFilePath():
    return sys.argv[1][:-POD_FILENAME_LEN]

# 目标文件上级目录名
def podFileDirectoryName():
    return sys.argv[1][:-8].split('/')[-1]

# 主要
def main():
    # 输入参数数量错误直接返回错误
    if 2 != len(sys.argv):
        print('Error：Count of parameters is not correct!')
        exit(ERROR_PARAMETERS_COUNT)

    # 输入文件不是 Podfile 直接返回错误
    if True != sys.argv[1].endswith('Podfile'):
        print('Error: Illegal parameters!')
        exit(ERROR_PARAMETERS_TYPE)

    # 判断 Pods 目录下的 Manifest.lock 是否存在，否则返回错误
    manifestFileName = sys.argv[1][:-4] + 's/Manifest.lock'
    if True != os.path.exists(manifestFileName):
        print('Error: Please run `pod install` first!')
        exit(ERROR_NEED_PODS)

    # 判断目标目录下的 EFPAConfig.json 是否存在，如果不存在的话，则使用默认的配置文件
    configFileName = podFilePath() + '/EFPAConfig.json'
    configString = '''
    {
        "config": {
            "categories": ["Other"],
            "categoryRegexes": [".*"]
        }
    }
    '''
    if True == os.path.exists(configFileName):
        cc = open(podFilePath() + "EFPAConfig.json", "r+")
        configString = cc.read()
        cc.close()

    # 读取 PODS 依赖关系并生成依赖关系数组
    manifestPodlist = readManifestPodListFromFile(manifestFileName)
    # ManifestPodClass.printList(manifestPodlist)
    podlist = generatePodListFromList(manifestPodlist)
    # PodClass.printList(podlist)

    # 生成依赖关系页面
    generateDependencyGraph(podlist, configString)

# 执行
if __name__ == "__main__":
    main()
