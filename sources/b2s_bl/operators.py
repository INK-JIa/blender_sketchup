import bpy, os
from .utils import *


class ExportToSketchUp(bpy.types.Operator):
    bl_idname = "export.send_to_sketchup"
    bl_label = "发送到 SketchUp"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if not selected_objects:
            self.report({"WARNING"}, "请先选择对象.")
            return {"CANCELLED"}

        export_path = get_prefs().export_path
        file_path = os.path.join(export_path, "fromblender.glb")

        # 使用新的 GLTF 导出选项
        bpy.ops.export_scene.gltf(
            filepath=file_path,
            use_selection=True,
            export_format="GLB",
            export_apply=True,  # 应用修改器
        )

        self.report({"INFO"}, f"导出至 {file_path}")
        return {"FINISHED"}


class B2S_ImportFrom_SKP_file(bpy.types.Operator):
    bl_idname = "import.import_from_skp_file"
    bl_label = "导入缓存skp文件"
    bl_description = "调用外部插件,从B2S缓存文件夹中导入skp组件文件"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return hasattr(bpy.ops.import_scene, "skp")

    def execute(self, context):
        if hasattr(bpy.ops.import_scene, "skp"):
            try:
                bpy.ops.import_scene.skp(
                    filepath=str(get_b2s_temp_dir(self) / "tmp.skp")
                )
            except:
                self.report({"ERROR"}, "导入失败!")
        else:
            self.report({"ERROR"}, "请先安装sketchup_importer插件!")
        return {"FINISHED"}


class ImportFromSketchUp(bpy.types.Operator):
    bl_idname = "import.import_su_to_blender"
    bl_label = "导入 SU 到 Blender"

    def execute(self, context):
        export_path = get_prefs().export_path
        file_path = os.path.join(export_path, "toblender.glb")

        if not os.path.exists(file_path):
            self.report({"WARNING"}, "文件不存在!")
            return {"CANCELLED"}

        # 导入模型
        bpy.ops.import_scene.gltf(filepath=file_path)
        self.report({"INFO"}, f"导入自 {file_path}")

        # 获取导入后选中的对象
        imported_objects = bpy.context.selected_objects

        # 记录空物体
        empty_objects = [obj for obj in imported_objects if obj.type == "EMPTY"]

        # 合并同一父级下的网格对象
        parent_meshes = {}
        for obj in imported_objects:
            if obj.type == "MESH":
                if obj.parent not in parent_meshes:
                    parent_meshes[obj.parent] = []
                parent_meshes[obj.parent].append(obj)

        # 执行合并操作
        for parent, meshes in parent_meshes.items():
            if len(meshes) > 1:  # 仅当有多个网格体时合并
                bpy.ops.object.select_all(action="DESELECT")  # 先取消选择所有
                for mesh in meshes:
                    mesh.select_set(True)

                bpy.context.view_layer.objects.active = meshes[
                    0
                ]  # 设置第一个为活跃对象
                bpy.ops.object.join()  # 合并选中的网格对象

        # 再次获取当前选中的对象集合
        imported_objects = bpy.context.selected_objects

        # 清除父级并保持变换
        for obj in list(imported_objects):  # 使用list复制，以避免修改当前集合
            if obj.parent:
                bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")

        # 删除记录的空物体
        for empty in empty_objects:
            # 直接删除选中的空物体
            if empty.name in bpy.data.objects:
                bpy.data.objects.remove(bpy.data.objects[empty.name], do_unlink=True)

        # 设置材质折射率（IOR）为1.5
        default_ior = 1.5
        for mat in bpy.data.materials:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == "BSDF_PRINCIPLED":
                        node.inputs["IOR"].default_value = default_ior

        return {"FINISHED"}


CLASSES = [B2S_ImportFrom_SKP_file, ExportToSketchUp, ImportFromSketchUp]
class_register, class_unregister = bpy.utils.register_classes_factory(CLASSES)


def register():
    class_register()


def unregister():
    class_unregister()
