# 简介
这是一个从blender到sketchup文件互相传输的插件,仅支持Windows系统。
# 注意事项
### 软件运行环境
- blender 4.2 以及 sketchup 2024
# 软件安装
### blender
- 联网安装:
    - 获取扩展面板,添加远程存储库https://blender4.com/xz
    - 刷新并搜索b2s安装即可
- 离线安装:
    - 下载Blender_extension目录下的b2s.zip文件
    - bl插件偏好设置面板,点击"从磁盘安装",选择下载的"b2s.zip"文件
    
### SketchUp
- 离线安装:
    - 下载SketchUp_plugin目录下的b2s.rbz文件
    - 在SketchUp中,点击"扩展管理器",选择下载的"b2s_*.rbz"文件

# 其他注意事项
- 默认数据中转目录为%APPDATA%\Local\b2s_temp\
- 默认数据中转目录可手动指定(bl和su需设置相同位置才能正常使用)

# 声明
- 本人不是专业的程序员，此插件仅为交流学习使用，希望专业的你能够完善这个插件！

- 目前sketchup中发送到ble 8nder，还未实现从选定对象发送，因此你有可能需要新开一个窗口来作为文件交换使用！

（如想要编辑各插件，请下载sources文件夹下对应文件！）

***
### [查看更新日志](./CHANGELOG.md)