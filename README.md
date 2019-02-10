![](assets/headimage.png)

<p align="center">
    <a href="https://pypi.org/project/efpodsanalyzer/">
        <img src="https://badge.fury.io/py/efpodsanalyzer.svg">
    </a>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/language-Python-2e6fa0.svg">
    </a>
    <a href="https://codebeat.co/projects/github-com-eyrefree-efpodsanalyzer-master">
        <img src="https://codebeat.co/badges/67a3cc17-24fb-4c3d-b94c-61e17eea08cc"/>
    </a>
    <a href="https://raw.githubusercontent.com/EyreFree/EFPodsAnalyzer/master/LICENSE">
        <img src="https://img.shields.io/badge/license-GPLv3-000000.svg">
    </a>
    <a href="https://twitter.com/EyreFree777">
        <img src="https://img.shields.io/badge/twitter-@EyreFree777-blue.svg?style=flat">
    </a>
    <a href="http://weibo.com/eyrefree777">
        <img src="https://img.shields.io/badge/weibo-@EyreFree-red.svg?style=flat">
    </a>
    <a href="https://raw.githubusercontent.com/EyreFree/EFQRCode/assets/icon/MadeWith%3C3.png">
        <img src="https://img.shields.io/badge/made%20with-%3C3-orange.svg">
    </a>
</p>

EFPodsAnalyzer is a Python script that is used to help us sort out the CoaoaPods library dependency relationship. It can generate clear Pods dependency graph with only one command, which will help us in dependency sorting / component cleaning.

> [中文介绍](/README_CN.md)

## Preview

The more the Pods library is, the more complex the library is, the more it is used to get the tool, for example, the modularized item; conversely, if the project dependency is very few and the dependency relation is very simple, there is no need for this tool. The dependency graph of a project of our company is as follows, looks like a shit:

![](assets/overview.png)

## Requirements

- Python 2.7

## Installation

### PyPI

If you have `pip` installed on your device, you can install the latest version of this tool directly with the following commands:

```
sudo pip install efpodsanalyzer --upgrade
```

### Manual

Download this project, or execute the following commands to Clone this project:

```
git clone git@github.com:EyreFree/EFPodsAnalyzer.git
```

## Usage

### PyPI

1. First, ensure that your project has been operated on `pod install` and successfully generated the Pods directory;
2. Install `efpodsanalyzer` on your device with `pip`;
3. Classify the dependent libraries according to the specific circumstances of the projects to be analyzed, and give the regex of each category separately, then write the rules to the `EFPAConfig.json` file under the directory which contains the target `Podfile`;
4. Execute the following commands for the generation of the dependency graph:

```
sudo efpodsanalyzer [Target Podfile file path]
```

5. You can check the output of the terminal. If you see the following log, you can open the generated file `index.html` in the path with your browser:

```
Dependency graph generated: .../EFPADiagram/index.html
```

If there is any error, please deal with the corresponding error information, or you can make a PR or an Issue.

### Manual

1. First, ensure that your project has been operated on `pod install` and successfully generated the Pods directory;
2. The content of this tool has been fully downloaded to the local area;
3. Classify the dependent libraries according to the specific circumstances of the projects to be analyzed, and give the regex of each category separately, then write the rules to the `EFPAConfig.json` file under the directory which contains the target `Podfile`;
4. Execute the following commands for the generation of the dependency graph:

```
python [EFPodsAnalyzer.py file path] [Target Podfile file path]
```

5. You can check the output of the terminal. If you see the following log, you can open the generated file `index.html` in the path with your browser:

```
Dependency graph generated: .../EFPADiagram/index.html
```

If there is any error, please deal with the corresponding error information, or you can make a PR or an Issue.

## Example

Here we take [Coding's open source iOS client](https://github.com/Coding/Coding-iOS) as an example to show you the complete use of this tool:

1. First, install `efpodsanalyzer` on your device with `pip`.
2. Then download the Coding iOS project to local, and perform `pod install` operation;
3. Because the dependency of the Coding client is basically not classified, which is all the third party library. Therefore, for demonstration purposes, I divide it into three categories: the library with the beginning of 'M', the library ending with 'Kit' and the others. The `EFPAConfig.json` is as follows:

```
{
    "config": {
        "categories": ["M-prefixed Libraries", "Library ending with Kit", "Other"],
        "categoryRegexes": ["^M.*", ".*(Kit)$", ".*"]
    }
}
```

4. The command to generate diagram is as follows:

```
sudo efpodsanalyzer /Users/eyrefree/Documents/iOS_GitHub/Coding-iOS/Podfile
```

5. The final dependency graph is generated as follows:

![](assets/example.png)

You can also [view it online](https://eyrefree.github.io/EFPodsAnalyzer/index.html):

- Clicking on the top class name can control the display and hiding of the class;
- The mouse can be suspended on the node to display the node name;
- The mouse can be suspended on the line between two nodes to display the relationship of them.

## Todo

- Determine whether the dependency needs to be removed, according to the header file reference;
- Determine whether the dependency needs to be removed, depending on the class dependency;
- More style of diagrams.

## Other

1. The view of dependency graph is based on [ECharts](https://github.com/ecomfe/echarts) and [xml2json](https://github.com/abdmob/x2js), thanks for their work!
2. Code of this tool can be packaged / released using the following commands. People who needs to build a custom version can make some self exploration(Under the root directory of this project):

 ```
rm -rf dist/*;
python setup.py sdist bdist_wheel;
twine upload dist/efpodsanalyzer*;
```

## Author

EyreFree, eyrefree@eyrefree.org

## License

![](https://www.gnu.org/graphics/gplv3-127x51.png)

EFPodsAnalyzer is available under the GPLv3 license. See the LICENSE file for more info.
