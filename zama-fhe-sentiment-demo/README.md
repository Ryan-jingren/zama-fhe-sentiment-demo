# 文本情感分类同态加密演示

这是一个用于演示文本情感分类同态加密（FHE）的教学示例，基于 Zama 的 Concrete-ML。大家可以参考下列步骤自行部署。

原作者与项目来源：
- [Zama 官方 Hugging Face 演示与源码](https://huggingface.co/spaces/zama-fhe/encrypted_sentiment_analysis)
- [Concrete-ML](https://github.com/zama-ai/concrete-ml)

本目录提供中文部署说明、官方演示嵌入页面以及源码导入工具。它不是 Zama 官方维护的仓库，也不表示 Zama 为本项目背书。

## 两种使用方式

### 直接使用官方计算服务

用浏览器打开 `index.html`，或者把它部署到静态网站。在网页内可体验生成密钥、编码与加密、密文推理以及解密情感分类结果。计算由官方 Space 承担，无需创建自己的付费 Space。页面加载和排队情况取决于官方服务及当地网络。

### 自行运行 Python 演示

先确认 `upstream/` 和 `SOURCE_MANIFEST.json` 已存在；它们由仓库中的 **Import Zama FHE sentiment demo source** 工作流下载。若工作流尚未完成，可在本机运行：

```sh
python3 import_upstream.py
```

工具会从同一个确定的官方提交下载源码、笔记本及 `deployment/` 模型文件，记录原始 SHA-256，排除运行时密钥与临时数据。它不会执行下载的代码，已有源码目录也不会被自动覆盖。

参考上游的 Python 3.10 环境，在支持 Concrete-ML 的系统中运行：

```sh
cd upstream
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip wheel setuptools
python -m pip install -r requirements.txt
mkdir -p .fhe_keys tmp
python app.py
```

访问程序打印的本地 Gradio 地址。保留整个 `deployment/` 目录，不要只复制 `app.py`。模型预处理还可能下载 Transformer 权重，需要可用网络。原始依赖版本较旧，安装及运行兼容性需要在目标机器验证；本仓库不声称已完成端到端推理验证。

如果部署到自己的 Hugging Face Space，可以使用原 Space 的 **Duplicate this Space** 功能，选择 Public，并按账户页面确认套餐与资源费用。此步骤不等同于嵌入官方演示。

## 数据处理边界

原演示的“客户端”代码在 Python 服务上运行：输入文本、密钥生成与解密并非全部发生在浏览器内。它演示的是 FHE 推理流程，不是浏览器端端到端隐私产品。体验时使用虚构英文文本，不要输入真实机密数据。静态页面不能独立执行 Concrete-ML。

## 来源、许可证与可复现性

下载版本记录在 `SOURCE_MANIFEST.json`，所有原始作者署名及上游存在的许可证文件均保留在 `upstream/`。笔记本输出已移除，因此文件哈希记录描述下载时的原文件。

Concrete-ML 自身使用 BSD 3-Clause Clear License，详见其[官方许可证](https://github.com/zama-ai/concrete-ml/blob/main/LICENSE)。它不自动决定 Hugging Face 仓库全部文件、模型与数据集的许可；本目录不为上游文件重新授予许可证。再分发和自行部署时应遵循对应上游文件及依赖的适用条款。
