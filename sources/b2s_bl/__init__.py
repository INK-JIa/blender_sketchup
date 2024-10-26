import bpy
from .utils import *
from bpy.props import StringProperty
from . import operators

ADDON_ID = "b2s"

class SketchUpPanel(bpy.types.Panel):
    bl_label = "SketchUp 导入导出"
    bl_idname = "PANEL_PT_sketchup"
    bl_space_type = 'VIEW_3D'  
    bl_region_type = 'UI'       
    bl_category = ADDON_ID.upper()  

    def draw(self, context):
        layout = self.layout
        col = layout.box().column(align=True)
        col.operator("import.import_su_to_blender")
        col.operator("import.import_from_skp_file")
        col.separator(factor = 0.5)
        col.operator("export.send_to_sketchup")
        

class SketchUpSettingsPanel(bpy.types.AddonPreferences):
    bl_idname = __package__     # 4.2中API更换，获取该extension的id_name为__package__

    export_path: StringProperty(name="Export Path",default=str(get_cache_dir()),subtype='DIR_PATH') # type: ignore
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "export_path", text="Export Path")

preview_collections = {}
def load_custom_b2s_icon():
    icons_directory = Path(__file__).parent / "icons"
    pcoll = bpy.utils.previews.new()
    for path in icons_directory.glob("*.png"):
        name = path.stem.upper()  # 使用文件名（不含扩展名）作为键名
        print("Loading icon:", name)
        pcoll.load(name, str(path), "IMAGE")
    preview_collections["b2s"] = pcoll
    
def get_icon_id(pic_name):
    # print("Available icons:", list(preview_collections["b2s"].keys()))
    return preview_collections["b2s"][pic_name.upper()].icon_id


def b2s_menu_header(self, context):
    b2s_menu_header.f(self, context)
    
    row = self.layout.row()
    box = row.box()
    sub_row = box.row(align=True)
    sub_row.scale_x = 1
    sub_row.operator("import.import_su_to_blender",  text="",icon_value = get_icon_id("from_su_comp"))
    sub_row.operator("import.import_from_skp_file",  text="",icon_value = get_icon_id("from_su"))
    sub_row.separator(factor=0.2)
    sub_row.operator("export.send_to_sketchup", text="",icon_value = get_icon_id("to_su"))
    
b2s_menu_header.f = bpy.types.TOPBAR_HT_upper_bar.draw_right
    
CLASSES = [
    SketchUpPanel,
    SketchUpSettingsPanel
]
class_register,class_unregister = bpy.utils.register_classes_factory(CLASSES)

def register():
    operators.register()
    class_register()
    load_custom_b2s_icon()
    bpy.types.TOPBAR_HT_upper_bar.draw_right = b2s_menu_header
    translate_register()

def unregister():
    bpy.types.TOPBAR_HT_upper_bar.draw_right = b2s_menu_header.f
    bpy.utils.previews.remove(preview_collections["b2s"])
    preview_collections.clear()
    class_unregister()
    operators.unregister()
    translate_unregister()

if __name__ == "__main__":
    register()
