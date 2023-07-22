# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Shape Key Swapper",
    "description": "Adds a button with the name: (Swap Vertices at Shape Key Value) to the Shape Keys menu. It swap the vertex positions of a active shape key in the 0 and 1 value position.",
    "author": "Marek Hanzelka",
    "version": (1, 0, 1),
    "blender": (3, 6, 0),
    "location": "Properties > Data > Shape Keys",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}

import bpy

def swap_vertices_at_shape_key_value(self, context):
    # Get the active object
    obj = bpy.context.object

    # Get the shape keys
    shape_keys = obj.data.shape_keys

    # Get the shape keys to swap (The selected shape key)
    shape_key_index = bpy.context.object.active_shape_key_index
    shape_key = shape_keys.key_blocks[shape_key_index]

    # Set the active blend shape to 0 (Basis)
    bpy.context.object.active_shape_key_index = 0

    # Toggle edit mode
    bpy.ops.object.editmode_toggle()

    # Select all
    bpy.ops.mesh.select_all(action='SELECT')

    # Do the blend from shape operation from the shape the user selected
    bpy.ops.mesh.blend_from_shape(shape=shape_key.name, blend=1.0, add=True)

    # Select the key that the user chose
    bpy.context.object.active_shape_key_index = shape_key_index

    # Do the blend from shape operation from the shape the user selected
    bpy.ops.mesh.blend_from_shape(shape=shape_key.name, blend=-2.0, add=True)

    # Toggle object mode
    bpy.ops.object.editmode_toggle()

    self.report({'INFO'}, "Shape Key Vertices Swapped!")
    return {'FINISHED'}

def add_swap_mesh_entry(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("object.swap_vertices_at_shape_key_value", text="Swap Vertices at Shape Key Value", icon="UV_SYNC_SELECT")

# Add the operator and entry to the shape key context menu
def register():
    bpy.utils.register_class(SwapMeshAtShapeKeyValueOperator)
    bpy.types.MESH_MT_shape_key_context_menu.append(add_swap_mesh_entry)

# Remove the operator and entry from the shape key context menu
def unregister():
    bpy.utils.unregister_class(SwapMeshAtShapeKeyValueOperator)
    bpy.types.MESH_MT_shape_key_context_menu.remove(add_swap_mesh_entry)

# Operator class
class SwapMeshAtShapeKeyValueOperator(bpy.types.Operator):
    bl_idname = "object.swap_vertices_at_shape_key_value"
    bl_label = "Swap Vertices at Shape Key Value"
    bl_description = "Swap the vertex positions of the active shape key in the 0 and 1 value"

    def execute(self, context):
        return swap_vertices_at_shape_key_value(self, context)
        
    
    @classmethod
    def poll(cls, context):
        # Enable the option only in object mode
        return context.object and context.object.mode == 'OBJECT'


if __name__ == "__main__":
    register()
