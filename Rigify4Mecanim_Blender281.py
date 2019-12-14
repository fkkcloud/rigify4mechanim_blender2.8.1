bl_info = {
    "name": "Rigify to Unity",
    "category": "Rigging",
    "description": "Change Rigify rig into Mecanim-ready rig for Unity",
    "location": "At the bottom of Rigify rig data/armature tab",
    "blender":(2,80,0)
}

import bpy
import re

class UnityRigify_Panel(bpy.types.Panel):
    bl_label = "Unity to Rigify converter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}

    
    @classmethod
    def poll(self, context):
        if context.object and context.object.type == 'ARMATURE':
            return True
    
    def draw(self, context):
        self.layout.operator("rig4mec.convert2rigify")        
        


class UnityMecanim_Panel(bpy.types.Panel):
    bl_label = "Rigify to Unity converter"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        if context.object and context.object.type == 'ARMATURE':
            return True
    
    def draw(self, context):
        self.layout.operator("rig4mec.convert2unity")
        self.layout.prop(context.object, "myfile_path")
        self.layout.prop(context.object, "myapply_tr")
        self.layout.operator("rig4mec.export2fbx")
        #context.object.myapply_tr = True;
        
        
class UnityMecanim_Convert2Unity(bpy.types.Operator):
    bl_idname = "rig4mec.convert2unity"
    bl_label = "Convert to Unity rig"
    
    def execute(self, context):
        ob = bpy.context.object
        porg = re.compile('ORG-*')
        for object in ob.data.bones:
            object.use_deform = False
        for object in ob.data.bones:
            if porg.match(object.name):
                object.use_deform = True
        ob.data.bones['ORG-heel.L'].use_deform = False
        ob.data.bones['ORG-heel.02.L'].use_deform = False
        ob.data.bones['ORG-heel.R'].use_deform = False
        ob.data.bones['ORG-heel.02.R'].use_deform = False
        self.report({'INFO'}, 'Unity ready rig!')                

        return{'FINISHED'}

class UnityMecanim_Convert2Rigify(bpy.types.Operator):
    bl_idname = "rig4mec.convert2rigify"
    bl_label = "Convert to Rigify rig"
    
    def execute(self, context):
        ob = bpy.context.object
        porg = re.compile('DEF-*')
        for object in ob.data.bones:
            object.use_deform = False
        for object in ob.data.bones:
            if porg.match(object.name):
                object.use_deform = True
        self.report({'INFO'}, 'Rigify ready rig!')                

        return{'FINISHED'}
    
class UnityMecanim_Export2FBX(bpy.types.Operator):
    bl_idname = "rig4mec.export2fbx"
    bl_label = "Export to FBX file"
    
    
    def execute(self, context):
        ob = bpy.context.object
        for o in ob.children:
            o.select_set(True)
            
        fbxout = bpy.path.abspath(ob.myfile_path)
        myApplyTr = ob.myapply_tr
                
        bpy.ops.export_scene.fbx(filepath=fbxout, use_selection=True, use_armature_deform_only=True, bake_space_transform=myApplyTr, apply_unit_scale=False)
        self.report({'INFO'}, 'Rigged character exported!')                

        return{'FINISHED'}


def register():
    #properties
    bpy.types.Object.myfile_path = bpy.props.StringProperty(name="Export file", subtype="FILE_PATH")
    bpy.types.Object.myapply_tr = bpy.props.BoolProperty(name="!Apply Transform!", default=True)
    #classes     
    bpy.utils.register_class(UnityRigify_Panel)
    bpy.utils.register_class(UnityMecanim_Panel)
    bpy.utils.register_class(UnityMecanim_Convert2Unity)
    bpy.utils.register_class(UnityMecanim_Convert2Rigify)
    bpy.utils.register_class(UnityMecanim_Export2FBX)
    
    
def unregister():
    #classes
    bpy.utils.unregister_class(UnityRigify_Panel)
    bpy.utils.unregister_class(UnityMecanim_Panel)
    bpy.utils.unregister_class(UnityMecanim_Convert2Unity)
    bpy.utils.unregister_class(UnityMecanim_Convert2Rigify)
    bpy.utils.unregister_class(UnityMecanim_Export2FBX)
    #properties
    del bpy.types.Object.myfile_path
    del bpy.types.Object.myapply_tr
     
    

    
#bpy.utils.register_module(__name__)

