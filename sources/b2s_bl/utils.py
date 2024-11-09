from pathlib import Path
import os, csv, codecs, bpy, sys

ADDON_ID = "b2s"


def get_prefs():
    return bpy.context.preferences.addons[__package__].preferences


def contains_chinese(string):
    """检测字符串中是否包含中文字符"""
    for ch in string:
        if "\u4e00" <= ch <= "\u9fff":
            return True
    return False


def get_cache_dir():
    cache_dir = None
    if sys.platform == "win32":
        cache_dir = Path.home() / 'Documents'
    else:
        print("您的系统不支持自动缓存路径，请手动指定缓存文件夹!")
        return ''

    if contains_chinese(str(cache_dir)):
        print("用户名包含中文字符，请手动指定缓存文件夹!")
        return cache_dir



def get_b2s_temp_dir():
    if get_cache_dir() != None:
        b2s_temp_dir = get_cache_dir()/'blendsu'
        if b2s_temp_dir.exists():
            print(f"b2s 缓存文件夹已存在，路径为: {b2s_temp_dir}")
        else:
            b2s_temp_dir.mkdir(parents=True, exist_ok=True)
            print(f"b2s 缓存文件夹不存在，已创建")
        return b2s_temp_dir
    else:
        return ''


def GetTranslationDict():
    """翻译文件"""
    dict = {}
    path = os.path.join(os.path.dirname(__file__), "translation_dic.csv")

    with codecs.open(path, "r", "utf-8") as f:
        reader = csv.reader(f)
        dict["zh_HANS"] = {}
        for row in reader:
            if row:
                for context in bpy.app.translations.contexts:
                    dict["zh_HANS"][(context, row[0].replace("\\n", "\n"))] = row[
                        1
                    ].replace("\\n", "\n")
    return dict


def translate_register():
    try:
        bpy.app.translations.register(__package__, GetTranslationDict())
    except Exception as e:
        print(f"插件 {__package__.split('.')[-1]} 注册翻译错误:\n{e}")


def translate_unregister():
    try:
        bpy.app.translations.unregister(__package__)
    except Exception as e:
        print(f"插件 {__package__.split('.')[-1]} 取消注册翻译错误:\n{e}")
