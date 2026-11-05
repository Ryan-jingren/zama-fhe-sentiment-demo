# Zama 文本情感分类同态加密演示

这是一个可以用来演示文本情感分类同态加密（FHE）的教学项目，大家可以参考说明自行部署。

- [官方源码和模型文件](zama-fhe-sentiment-demo/upstream/)
- [中文部署说明](zama-fhe-sentiment-demo/README.md)
- [演示嵌入页面](zama-fhe-sentiment-demo/index.html)
- [来源版本和文件校验清单](zama-fhe-sentiment-demo/SOURCE_MANIFEST.json)
- [官方演示](https://huggingface.co/spaces/zama-fhe/encrypted_sentiment_analysis)

## 迁移状态

已导入官方 Space 的 14 个源码与模型文件，包括 Python 程序、训练笔记本、依赖清单、编译样本以及客户端和服务端部署模型。

来源提交：`5328edf819e165e80f6419741b54fa8297dfc2b9`。

[自动导入与 Python 语法检查均已通过](https://github.com/Ryan-jingren/zama-fhe-sentiment-demo/actions/runs/41955091149)。未进行完整安装与端到端加密推理验证。运行时密钥、临时用户数据及笔记本输出已排除，文件原始校验值与处理说明记录于清单。

## 使用方式

下载本仓库，在支持 Concrete-ML 的 Python 3.10 环境中按照[中文说明](zama-fhe-sentiment-demo/README.md)运行；或者将嵌入页面部署为静态网站，使用官方 Space 提供的演示计算服务。GitHub 文件页面本身不会执行 HTML 或 Python。

原作者为 Zama；本仓库提供迁移、中文说明与嵌入页面，并非 Zama 官方维护项目。原演示在远端 Python 服务执行预处理和密钥操作，请使用虚构文本体验。上游代码、模型、数据及依赖仍遵循各自适用的许可条件，详见中文说明。
