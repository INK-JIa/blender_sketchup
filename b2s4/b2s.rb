# b2s.rb

# Plugin Name: b2s
# Author: 墨水
# Version: 1.0.1
# Description: 插件可以实现与blender的模型互相传输，视频说明在https://www.bilibili.com/video/BV1NPmPYCE79
# Copyright: © 2024 免费插件不得售卖

require 'sketchup.rb'
require 'extensions.rb'

# 创建编码块以定义扩展
module MyPlugin
  # 插件名称
  PLUGIN_NAME = "b2s(blender与su互导插件)"
  # 插件版本
  VERSION = "1.0.1"
  
  # 创建新的扩展类
  extension = SketchupExtension.new(PLUGIN_NAME, 'b2s')

  # 设置扩展的属性
  extension.description = "插件完全免费，可以实现与blender的模型互相传输，视频说明在https://www.bilibili.com/video/BV1NPmPYCE79"
  extension.version = VERSION
  extension.creator = "墨水er"
  
  # 将扩展注册到扩展管理器
  Sketchup.register_extension(extension, true)
end

# 加载其他 .rb 文件
require_relative 'b2s/01fromblender.rb'
require_relative 'b2s/02toblender.rb'
require_relative 'b2s/03split.rb'

# 添加菜单项或工具条
if defined?(Sketchup)
  unless file_loaded?(__FILE__)
    # 在工具条或者菜单中添加功能
    menu = UI.menu("Plugins").add_submenu("b2s")

    menu.add_item("从blender导入") {
      # 替换为你的实际功能
      from_blender()
    }
    menu.add_item("导出到blender") {
      # 替换为你的实际功能
      to_blender()
    }
    menu.add_item("解散嵌套组") {
      # 替换为你的实际功能
      explode_to_deepest_level()
    }

    toolbar = UI::Toolbar.new "b2s"

    # 添加 From Blender 按钮
    cmd1 = UI::Command.new("从blender导入") {
      from_blender()  # 调用函数
    }
    cmd1.tooltip = "从blender导入"
    cmd1.small_icon = "b2s/fromblender.png"
    cmd1.large_icon = "b2s/fromblender.png"
    toolbar.add_item cmd1

    # 添加 To Blender 按钮
    cmd2 = UI::Command.new("导出到blender") {
      to_blender()  # 调用函数
    }
    cmd2.tooltip = "导出到blender"
    cmd2.small_icon = "b2s/toblender.png"
    cmd2.large_icon = "b2s/toblender.png"
    toolbar.add_item cmd2

    # 添加 Explode to Deepest Level 按钮
    cmd3 = UI::Command.new("解散嵌套组") {
      explode_to_deepest_level()  # 调用函数
    }
    cmd3.tooltip = "解散嵌套组"
    cmd3.small_icon = "b2s/split.png"
    cmd3.large_icon = "b2s/split.png"
    toolbar.add_item cmd3

    # 显示工具栏
    toolbar.show
    file_loaded(__FILE__)  # 标记文件已加载
  end
end
