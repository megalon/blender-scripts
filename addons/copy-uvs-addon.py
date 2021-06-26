bl_info = {
    "name": "Copy UVs",
    "author": "@megalon2d",
    "version": (1, 1),
    "blender": (2, 90, 0),
    "location": "View3D > Object > Copy UVs",
    "description": "Copy uv and seam info between identical meshes",
    "warning": "This will not work unless the meshes are identical!",
    "doc_url": "https://github.com/megalon/blender-scripts",
    "category": "UVs",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

def copy_uvs(self, context):
    print("Starting copy_uvs script")
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    for obj in selected:
        # Loop through all polys in active obj
        for active_poly_index in range(len(active.data.polygons)):
            # Get loop indices from current obj
            for i in obj.data.polygons[active_poly_index].loop_indices:
                
                # Loop this indice refers to
                loop = obj.data.loops[i]
                # print("Loop index", loop.index, "points to vertex index", loop.vertex_index)
                
                # Get UV layers for active and current
                active_ul = active.data.uv_layers[0]
                current_ul = obj.data.uv_layers[0]
                
                current_ul.data[loop.index].uv = active_ul.data[loop.index].uv
                # print("  UV Map has coordinates", current_ul.data[loop.index].uv, "for this loop index")
                
        # Copy seams
        for active_edge_index in range(len(active.data.edges)):
            obj.data.edges[active_edge_index].use_seam = active.data.edges[active_edge_index].use_seam


class OBJECT_OT_copy_uvs(Operator, AddObjectHelper):
    """Copy the UVs of the object to another"""
    bl_idname = "mesh.copy_uvs"
    bl_label = "Copy UVs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        copy_uvs(self, context)

        return {'FINISHED'}


# Registration
def copy_uvs_button(self, context):
    self.layout.operator(
        OBJECT_OT_copy_uvs.bl_idname,
        text=OBJECT_OT_copy_uvs.bl_label,
        icon='UV_SYNC_SELECT')

def register():
    bpy.utils.register_class(OBJECT_OT_copy_uvs)
    bpy.types.VIEW3D_MT_object.append(copy_uvs_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_copy_uvs)
    bpy.types.VIEW3D_MT_object.remove(copy_uvs_button)


if __name__ == "__main__":
    register()
