# MyAIPlus 严选 · 新代理开站与引流出单交互式指南

> 🌐 **在线交互教程网址**：[https://xjiaming644-del.github.io/myaiplus-agent-guide/](https://xjiaming644-del.github.io/myaiplus-agent-guide/)  
> 🛒 **官方总店**：[https://myaiplus.store](https://myaiplus.store) ｜ **代理开通入口**：[https://myaiplus.store/user/group/index](https://myaiplus.store/user/group/index)（限时特价 **¥9.9** 开通「至尊代理」赠送顶级分销权限）  
> 💬 **店主 / 代理核验微信**：`xjmazh`（添加备注：`代理咨询` 或 `AI合作`）

---

## 核心特性

- **双视图交互体验（浅色默认 + 深色模式一键切换）**：首页总览搜索 + Bento 卡片导航；点击进入 **4 阶段共 13 步三栏交互式向导**，左侧进度目录 + 右侧实时小提示，全部进度仅保存在本地浏览器 `localStorage`。
- **内置「我的分站一键换名器」防误发**：填入代理自己的店铺名、独立域名、微信号和下级代理门槛价，全站朋友圈、小红书、闲鱼暗语、群置顶与 6 大客服话术实时替换并高亮未填占位符。
- **独立分站收益与核账闭环**：详述 `¥9.9` 开通顶级分销（扣除 `5%` 手续费后 `95%` 实收 `¥9.41` 进「硬币」账户）+ 下级出单 `Tab 2 会员等级加价` 管道收益 + 「我的账单 → 分站会员等级收入」防误会查账路径。
- **严格合规护栏**：内置绝对合规红线提示与一键复制拒答话术，严禁推荐、提供或教学任何 VPN / 代理 / 网络加速工具。

---

## 仓库目录结构

```text
myaiplus-agent-guide/
├── .nojekyll                                              # 禁用 Jekyll，原样高速托管静态单页
├── index.html                                             # 100% 离线/在线单文件交互式教程网页
├── docs/
│   ├── 00_新人必读_使用说明.txt                            # 新手 10 行开箱使用说明
│   ├── 01_MyAIPlus_新代理极速开站与合规手册_对外脱敏版.md    # 独立分站 4 步实操、四梯队定价、核账防坑与红线
│   └── 02_新代理当天出单_引流与成交文案大礼包.md            # 店铺公告、朋友圈/小红书/闲鱼/群与客服 6 大话术
├── scripts/
│   └── build_agent_kit.py                                 # 零第三方依赖的单页网页、文档与转发 ZIP 生成器
└── tests/
    └── test_agent_kit.py                                  # 脱敏拦截、13 步路由完整性与 JS 语法单元测试
```

---

## 本地生成与测试

需要 Python 3.10+（零第三方包依赖）；若运行 JS 语法校验单元测试需安装 Node.js：

```bash
# 重新生成 index.html 与 docs/ 文档
python scripts/build_agent_kit.py

# 若需同时打包可直接微信转发的新代理 ZIP 大礼包
python scripts/build_agent_kit.py --zip-out ./dist/MyAIPlus_新代理入营大礼包.zip

# 运行全部单元测试（含通用敏感词防泄露、JSON 路由与 node --check JS 语法校验）
python -m unittest discover -s tests -v
```
