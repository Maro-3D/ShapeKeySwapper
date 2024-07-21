# This program is free software: 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Shape Key Swapper",
    "description": "Easily swap vertex positions between the 0 and 1 values of the active shape key with a single click. This tool adds a convenient button to the Shape Keys menu, streamlining the process of vertex position swapping in Blender.",
    "author": "Marek Hanzelka",
    "version": (1, 0, 2),
    "blender": (4, 2, 0),
    "location": "Properties > Data > Shape Keys",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"
}

import bpy

class SwapMeshAtShapeKeyValueOperator(bpy.types.Operator):
    """Operator for swapping vertex positions at shape key values"""
    bl_idname = "object.swap_vertices_at_shape_key_value"
    bl_label = "Swap Vertices at Shape Key Value"
    bl_description = "Swap the vertex positions of the active shape key between the 0 and 1 value positions"

    def execute(self, context):
        """Execute the operator"""
        obj = context.object

        # Check if object and shape keys exist
        if not obj or not obj.data.shape_keys:
            self.report({'ERROR'}, "No shape keys found")
            return {'CANCELLED'}

        # Get the shape keys and the selected shape key
        shape_keys = obj.data.shape_keys
        shape_key_index = obj.active_shape_key_index
        shape_key = shape_keys.key_blocks[shape_key_index]

        # Set the active shape key to the basis (0)
        obj.active_shape_key_index = 0

        # Enter edit mode
        bpy.ops.object.editmode_toggle()
        
        # Select all vertices
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Blend from the selected shape key to the basis
        bpy.ops.mesh.blend_from_shape(shape=shape_key.name, blend=1.0, add=True)

        # Set the active shape key back to the selected one
        obj.active_shape_key_index = shape_key_index
        
        # Blend from the basis to the selected shape key
        bpy.ops.mesh.blend_from_shape(shape=shape_key.name, blend=-2.0, add=True)
        
        # Exit edit mode
        bpy.ops.object.editmode_toggle()

        # Inform the user that the operation was successful
        self.report({'INFO'}, "Shape Key Vertices Swapped!")
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context):
        """Check if the operator can be executed"""
        return (context.object and context.object.mode == 'OBJECT' and
                context.object.data.shape_keys is not None and
                len(context.object.data.shape_keys.key_blocks) > 1)


def add_swap_mesh_entry(self, context):
    """Add the operator to the shape key context menu"""
    layout = self.layout
    layout.separator()
    layout.operator(SwapMeshAtShapeKeyValueOperator.bl_idname, text="Swap Vertices at Shape Key Value", icon="UV_SYNC_SELECT")


def register():
    """Register the operator and menu entry"""
    bpy.utils.register_class(SwapMeshAtShapeKeyValueOperator)
    bpy.types.MESH_MT_shape_key_context_menu.append(add_swap_mesh_entry)


def unregister():
    """Unregister the operator and menu entry"""
    bpy.utils.unregister_class(SwapMeshAtShapeKeyValueOperator)
    bpy.types.MESH_MT_shape_key_context_menu.remove(add_swap_mesh_entry)


if __name__ == "__main__":
    register()
