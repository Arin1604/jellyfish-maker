import importlib
import jelly_fish_maker
importlib.reload(jelly_fish_maker)
from jelly_fish_maker import JellyFishMaker
from maya import cmds

class TentacleMakerUI(BaseWindow):
    windowName = "Tentacle Maker"

    def __init__(self):
        super().__init__()

        self.Tentacle_Maker = None
        self.start = False

    def reload_modules(self):
        importlib.reload(lol)

    def buildUI(self):
        # Main column layout
        main_layout = cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Tentacle Maker Tool", align='center', font='boldLabelFont')

        # Geometry Management Section (Moved to the top)
        management_frame = cmds.frameLayout(label="Geometry Management", collapsable=True, marginHeight=10, marginWidth=10)
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Manage Tentacles", align='center', font='boldLabelFont')

        # Buttons for Geometry Management
        cmds.button(label="Make Tentacle", command=self.make_tentacles)
        cmds.button(label="Rig Tentacle", command=self.rig_tentacle)
        cmds.button(label="Delete Tentacles", command=self.delete_tents)
        cmds.button(label="Reset Tentacles", command=self.reset_tents)
        cmds.button(label="Select Tentacles", command=self.select_tents)
        cmds.button(label="Assign Material", command=self.assign_material)
        cmds.button(label="Animate", command=self.animate)
        cmds.button(label="Anchor", command=self.anchor)
        
        cmds.setParent('..')  # End Geometry Management Section

        # Geometry Generation Section
        generation_frame = cmds.frameLayout(label="Geometry Generation", collapsable=True, marginHeight=10, marginWidth=10)
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Generate Tentacles", align='center', font='boldLabelFont')

        # Number of Tentacles
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
        cmds.text(label="Number of Tentacles:")
        self.slider_number_tents = cmds.intSlider(min=1, max=30, step=1, dragCommand=self.update_tentacle_count_display)
        self.tentacle_count_display = cmds.text(label="5")  # Initial value display
        cmds.setParent('..')

        # Base Radius
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
        cmds.text(label="Base Radius:")
        self.base_rad = cmds.floatSlider(min=0, max=15, value=1, step=0.2, dragCommand=self.update_base_radius_display)
        self.base_radius_display = cmds.text(label="1.0")  # Initial value display
        cmds.setParent('..')

        # Tentacle Depth
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
        cmds.text(label="Tentacle Depth:")
        self.slider_tentacle_depth = cmds.intSlider(min=1, max=20, value=8, step=1, dragCommand=self.update_tentacle_depth_display)
        self.tentacle_depth_display = cmds.text(label="8")  # Initial value display
        cmds.setParent('..')

        # Rigging Smoothness (Converted to Dropdown)
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
        cmds.text(label="Rigging Smoothness:")
        self.rigging_smoothness_dropdown = cmds.optionMenu(changeCommand=self.update_rigging_smoothness_display)
        for i in range(1, 6):  # Values from 1-5
            cmds.menuItem(label=str(i))
        cmds.setParent('..')

        # Tentacle Displacement
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
        cmds.text(label="Tentacle Displacement:")
        self.slider_tentacle_displacement = cmds.intSlider(min=0, max=20, value=4, step=1, dragCommand=self.update_tentacle_displacement_display)
        self.tentacle_displacement_display = cmds.text(label="2.0")  # Initial value display
        cmds.setParent('..')

        cmds.setParent('..')  # End Geometry Generation Section

        # Geometry Editing Section
        editing_frame = cmds.frameLayout(label="Geometry Editing", collapsable=True, marginHeight=10, marginWidth=10)
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label="Edit Existing Geometry", align='center', font='boldLabelFont')

        # Modify Tentacle Scale
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
        cmds.text(label="Tentacle Scale:")
        self.slider = cmds.floatSlider(min=0, max=2, value=1, step=0.05, dragCommand=lambda value: [self.modify_tents(value), self.update_scale_display(value)])
        self.scale_display = cmds.text(label="1.0")  # Initial value display
        cmds.setParent('..')

        # Modify Tentacle Taper
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
        cmds.text(label="Tentacle Taper:")
        self.slider_taper = cmds.floatSlider(min=0, max=4, value=1, step=0.05, dragCommand=lambda value: [self.modify_tents_taper(value), self.update_taper_display(value)])
        self.taper_display = cmds.text(label="1.0")  # Initial value display
        cmds.setParent('..')

        # Modify Taper Point
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
        cmds.text(label="Taper Point:")
        self.slider_taper_point = cmds.floatSlider(min=0, max=1, value=1, step=0.025, dragCommand=lambda value: [self.modify_tents_taper_point(value), self.update_taper_point_display(value)])
        self.taper_point_display = cmds.text(label="1.0")  # Initial value display
        cmds.setParent('..')

        # Modify Taper Value
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2)
        cmds.text(label="Taper Value:")
        self.slider_taper_value = cmds.floatSlider(min=0, max=2, value=1, step=0.05, dragCommand=lambda value: [self.modify_tents_taper_val(value), self.update_taper_value_display(value)])
        self.taper_value_display = cmds.text(label="1.0")  # Initial value display
        cmds.setParent('..')

        cmds.setParent('..')

        # Close Button
        cmds.setParent(main_layout)
        cmds.button(label="Close", command=self.close)
    
    # Helper methods to update numeric displays
    def update_tentacle_count_display(self, value):
        cmds.text(self.tentacle_count_display, edit=True, label=str(int(value)))
        
        
        # self.make_tentacles()
    def update_rigging_smoothness_display(self, value):
        cmds.text(self.rigging_smoothness_dropdown, edit=True, label=str(int(value)))

        

    def update_base_radius_display(self, value):
        cmds.text(self.base_radius_display, edit=True, label=f"{value:.1f}")

    def update_tentacle_depth_display(self, value):
        cmds.text(self.tentacle_depth_display, edit=True, label=f"{value:.1f}")

    def update_tentacle_displacement_display(self, value):
        cmds.text(self.tentacle_displacement_display, edit=True, label=f"{value:.1f}")

    def update_scale_display(self, value):
        cmds.text(self.scale_display, edit=True, label=f"{value:.2f}")

    def update_taper_display(self, value):
        cmds.text(self.taper_display, edit=True, label=f"{value:.2f}")

    def update_taper_point_display(self, value):
        cmds.text(self.taper_point_display, edit=True, label=f"{value:.2f}")

    def update_taper_value_display(self, value):
        cmds.text(self.taper_value_display, edit=True, label=f"{value:.2f}")
    


    def animate(self, *args):
        # self.make_tentacles()
        # self.rig_tentacle()
        self.Tentacle_Maker.animate()
    
    def anchor(self, *args):
        self.Tentacle_Maker.attach_to_selected_joint()

    def assign_material(self, *args):
        self.Tentacle_Maker.assign_material()
        self.Tentacle_Maker.volume_render()


    def make_tentacles(self, *args):
        if self.start:
            self.delete_tents()
        num_tents = cmds.intSlider(self.slider_number_tents, query=True, value=True)
        base_rad = cmds.floatSlider(self.base_rad,query=True, value=True)
        scale = cmds.floatSlider(self.slider, query=True, value=True)
        taper = cmds.floatSlider(self.slider_taper, query=True, value=True)
        taper_point = cmds.floatSlider(self.slider_taper_point, query=True, value=True)
        taper_val = cmds.floatSlider(self.slider_taper_value, query=True, value=True)
        tent_depth = cmds.intSlider(self.slider_tentacle_depth, query=True, value=True)
        tent_disp = cmds.intSlider(self.slider_tentacle_displacement, query=True, value=True)
        rig_smoothness = int(cmds.optionMenu(self.rigging_smoothness_dropdown, query=True, value=True))

        self.Tentacle_Maker = JellyFishMaker(num_tents=num_tents, base_radius=base_rad, scale=scale, taper=taper, taper_point=taper_point, taper_val=taper_val, tent_len=tent_depth, tent_disp=tent_disp, rig=rig_smoothness)
        self.Tentacle_Maker.create_tentacle_geom(True)
        # self.start = True
        # # self.Tentacle_Maker.create_bezier_curve()
        # self.Tentacle_Maker.create_bezier_curve_spline()
    
    def rig_tentacle(self, *args):
        # New tentacle-making logic
        # self.delete_tents()
        rig_smoothness = int(cmds.optionMenu(self.rigging_smoothness_dropdown, query=True, value=True))

        self.Tentacle_Maker.rig_smooth = rig_smoothness
        self.Tentacle_Maker.create_bezier_curve_spline()  # Call the alternative function

    
    def modify_tents(self, scale):
        self.Tentacle_Maker.modify_tent_scale(scale)

    def delete_tents(self, *args):
        self.Tentacle_Maker.delete_geom()

    def select_tents(self, *args):
        self.Tentacle_Maker.select_tents()
    
    def reset_tents(self, *args):
        self.Tentacle_Maker.delete_geom()
        self.make_tentacles()
        # self.make_tentacle_2()

    def modify_tents_taper(self, taper):
        self.Tentacle_Maker.modify_tent_taper(taper)
    
    def modify_tents_taper_point(self, point):
        self.Tentacle_Maker.modify_tent_taper_point(point)
    
    def modify_tents_taper_val(self, taper_val):
        self.Tentacle_Maker.modify_tent_taper_value(taper_val)
    
    def reset(self, *args):
        print("Resetting tween")
        cmds.floatSlider(self.slider, edit=True, value = 50)