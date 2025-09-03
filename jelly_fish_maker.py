import maya.cmds as cmds
import random
import math

#name corresponds to the sweepShape associated with the tentacle, the sweep mesh creator not included here allows us to manipulate its geometry qualities
class Tentacle(object):
    """_summary_
        Our tentacle object, stores relevant fields for our tentacles. Can be modified.
    """
    def __init__(self, idx, curve_identifier,points=None, curves=None, geometry=None, ctrls=None):
        self.curves = curves
        self.points = points
        self.geometry = geometry
        self.ctrls = ctrls
        self.curve_identifier = curve_identifier
        self.idx = idx

    def get_name(self):
        return "-"

class JellyFishMaker(object):
    """_summary_
        The main jelly fish maker class. Creates tentacles as specified and stores an array of all active tentacles
    """

    def __init__(self, num_tents, scale, taper, taper_point, taper_val, base_radius=3, tent_len=8, tent_disp=4, rig = 1):
        self.num_tents =num_tents
        self.base_radius = base_radius
        self.scale = scale
        self.taper = taper
        self.taper_point = taper_point
        self.taper_val = taper_val
        self.tent_len = tent_len
        self.tent_disp = tent_disp

        #add inputs
        self.spline_spans = 4
        self.rig_smooth = rig

        self.tentacles = []
        self.global_ctrls = []

    def modify_tent_taper(self, taper):
        self.taper = taper
        for i in range(self.num_tents):
            cmds.setAttr("sweepMeshCreator{}.taper".format(i + 1), taper)

    def modify_tent_taper_point(self, taper_point):
        self.taper_point = taper_point
        for i in range(self.num_tents):
            cmds.setAttr("sweepMeshCreator{}.taperCurve[0].taperCurve_Position".format(i + 1), taper_point)

    def modify_tent_taper_value(self, taper_val):
        self.taper_val = taper_val
        for i in range(self.num_tents):
            cmds.setAttr("sweepMeshCreator{}.taperCurve[0].taperCurve_FloatValue".format(i + 1), taper_val)


    def modify_tent_scale(self, scale):
        self.scale = scale
        for i in range(self.num_tents):
            cmds.setAttr("sweepMeshCreator{}.scaleProfileX".format(i + 1), scale)
    
    def select_tents(self):
        for i in range(self.num_tents):
            curr_sweep = "sweep"

            if i == 0:
                # curr_curve += 
                sweep = 1
                curr_sweep = curr_sweep + str(sweep)
            
            else:
                sweep = 1 + i
                curr_sweep = curr_sweep + str(sweep)
            
            if cmds.objExists(curr_sweep):
                cmds.select(curr_sweep, add=True)  # Select the object
                
                print(f"{curr_sweep} has been selected.")
            else:
                print(f"{curr_sweep} does not exist.")
            


    def delete_geom(self):
        for i in range(self.num_tents):
            ##Note:
            #Curves are zero indexed
            #sweep's are NOT zero indexed

            curr_curve = "Bezier_Curve"
            curr_sweep = "sweep"

            if i == 0:
                # curr_curve += 
                sweep = 1
                curr_sweep = curr_sweep + str(sweep)
            
            else:
                curr_curve = curr_curve + str(i)
                sweep = 1 + i
                curr_sweep = curr_sweep + str(sweep)
            
            # object_to_delete = "sweep23"

            print("THIS IS THE CURRENT CURVE{} and ITS CORRESPONDING SWEEP{}".format(curr_curve, curr_sweep))

            if cmds.objExists(curr_sweep):
                cmds.select(curr_sweep, replace=True)  # Select the object
                cmds.delete()  # Delete the selected object
                print(f"{curr_sweep} has been deleted.")
            else:
                print(f"{curr_sweep} does not exist.")
            
            if cmds.objExists(curr_curve):
                cmds.select(curr_curve, replace=True)  # Select the object
                cmds.delete()  # Delete the selected object
                print(f"{curr_curve} has been deleted.")
            else:
                print(f"{curr_curve} does not exist.")

    def assign_material(self):

        shading_group = "lambertjpSG"
        for i in range(self.num_tents):
            ##Note:
            #Curves are zero indexed
            #sweep's are NOT zero indexed

            curr_curve = "Bezier_Curve"
            curr_sweep = "sweep"

            if i == 0:
                # curr_curve += 
                sweep = 1
                curr_sweep = curr_sweep + str(sweep)
            
            else:
                curr_curve = curr_curve + str(i)
                sweep = 1 + i
                curr_sweep = curr_sweep + str(sweep)
            
            if cmds.objExists(curr_sweep):
                cmds.sets(curr_sweep, edit=True, forceElement=shading_group)
            else:
                print(f"Geometry {curr_sweep} does not exist.")

    def volume_render(self):
        for i in range(self.num_tents):
            ##Note:
            #Curves are zero indexed
            #sweep's are NOT zero indexed
            
            curr_sweep = "sweepShape"

            if i == 0:
                # curr_curve += 
                sweep = 1
                curr_sweep = curr_sweep + str(sweep)
            
            else:
                sweep = 1 + i
                curr_sweep = curr_sweep + str(sweep)
            
            cmds.setAttr("{}.aiStepSize".format(curr_sweep), 0.1)
            cmds.setAttr("{}.aiVolumePadding".format(curr_sweep), 1)
    
    def close_ends(self):
        for tent in self.tentacles:
            curr_sweep = "sweep{}".format(tent.idx)


            if cmds.objExists(curr_sweep):
                cmds.select(curr_sweep, replace=True)  
                
            # Selects the object and closes the open tip
            cmds.polyCloseBorder(constructionHistory=False, name='closeBorderNode')

            
    def create_ik_spline_handle(self, joint_start, joint_end, name):
        """_summary_
        Uses the start and end joint to create a spline handle
        """
        ik_handle = cmds.ikHandle(solver='ikSplineSolver', sj=joint_start, ee=joint_end, n='tent{}_ikHandle'.format(name + 1), ns=self.spline_spans)
        spline_handle = ik_handle[0]
        spline_curve = ik_handle[2]
        spline_curve = cmds.rename(spline_curve, "tent_curve{}".format(name))
        cmds.getAttr( '{}.degree'.format(spline_curve) )
        return spline_handle, spline_curve

    def create_cluster(self, curve, tent_name):
        out_clstrs = []

        ctrlVerts = cmds.ls('{}.cv[:]'.format(curve), flatten = 1)

        
        for i,vert in enumerate(ctrlVerts):
            
            cluster = cmds.cluster(vert, n='tent{}_clstr{}'.format(tent_name,i + 1))
            print("AAAAAAAAAAAAAAAAAa{}".format(cluster))
            cluster_obj = cluster[0]
            cluster_handle = cluster[1] 

            cmds.setAttr(f"{cluster_handle}.visibility", False)
                    
            out_clstrs.append(cluster)

        return out_clstrs, ctrlVerts

    def create_controls(self, clusters, ctrlVerts, tent_name):
        out_ctrls = []
        r = self.tent_len

        i = 0

        for clstr, clust_pos in zip(clusters, ctrlVerts):
            print(clust_pos)
            i += 1
            r = 2 - (i * 0.2)
            print(clstr)
            
    
            clstr_pos = cmds.pointPosition(clust_pos)
            nurbs_circle_obj = cmds.circle(n='tentacle{}_cont{}'.format(tent_name, i + 1),c=clstr_pos, r=r, nr=(0, 1, 0))
            nurbs_circle = nurbs_circle_obj[0]
            cmds.xform(nurbs_circle, piv=clstr_pos, ws=True)
            print('This is the nurbs circle{} and this is the cluster{}'.format(nurbs_circle, clstr))
            # cmds.parent(nurbs_circle, clstr)
            cmds.parentConstraint(nurbs_circle, clstr[1], mo=True, weight=1)
            out_ctrls.append(nurbs_circle)
            self.global_ctrls.append(nurbs_circle)

        return out_ctrls
    
    def create_joints(self, points, name):
        out_joints = []
        for k,point in enumerate(points):
            out_joints.append(cmds.joint(n='tentacle{}_joint{}'.format(name + 1, k + 1),p=point))
        return out_joints

    def interpolate_points(self, point_array):
        """
        Interpolates the points in `point_array` and returns `len(point_array) * multiplier` evenly spaced points.

        Args:
            point_array (list of tuples): List of points (x, y, z) to be interpolated.
            multiplier (int): Number of interpolated points (how many times more points the output should have).

        Returns:
            list of tuples: Interpolated points, evenly spaced.
        """
        # Ensure the input array has at least 2 points to interpolate between
        if len(point_array) < 2:
            raise ValueError("point_array must have at least two points to interpolate.")

        # Initialize the result list with the first point
        interpolated_points = [point_array[0]]

        # Number of total points needed
        multiplier = self.rig_smooth
       
        total_points = len(point_array) * multiplier

        # For each pair of consecutive points in the original array
        for i in range(len(point_array) - 1):
            start_point = point_array[i]  # Current point (x, y, z)
            end_point = point_array[i + 1]  # Next point (x, y, z)
            
            # Calculate the step size for interpolation
            step = 1 / multiplier

            # Generate intermediate points
            for j in range(1, multiplier):
                t = j * step
                # Interpolate each coordinate (x, y, z) separately
                interpolated_point = (
                    start_point[0] + t * (end_point[0] - start_point[0]),
                    start_point[1] + t * (end_point[1] - start_point[1]),
                    start_point[2] + t * (end_point[2] - start_point[2]),
                )
                interpolated_points.append(interpolated_point)
            
            # Add the last point of the pair (avoiding duplicates)
            interpolated_points.append(end_point)

        return interpolated_points


    def create_tentacle_points(self, randomize):
        a = random.uniform(0, 2 * math.pi)  # Random angle between 0 and 2pi
        b = random.uniform(0.5, 1.5)        # Random scale factor for radius


        # Generate x, z coordinates for the starting points of the curve
        x = self.base_radius * math.sqrt(b) * math.cos(a)
        z = self.base_radius * math.sqrt(b) * math.sin(a)

        # Print x, z for debugging and to see the distribution
        print(f"Starting Point x: {x}, z: {z}")

        # if not randomize:
        #     x = 0
        #     z = 0

        # Add the base point for the curve
        point_i = (x, 0, z)  # Base point
        points = []
        points.append(point_i)

        for k in range(self.tent_len):
            # Randomize the vertical position (y) for variation
            ### ADD SLIDERS FOR THESE
            y = - (k+1) * 3  # Change the multiplier as needed for effect
            tentacle_x_disp = a = random.uniform(0, 2 * math.pi)

            if randomize:
                x += math.cos( tentacle_x_disp * self.tent_disp)
                z += math.sin(tentacle_x_disp * self.tent_disp)

            print("This is the tentacle, and this is the point")
            new_point = (x, y, z)
            
            points.append(new_point)
                
        return points
                

    def create_tentacle_geom(self, displace_tents):
        for i in range(self.num_tents):

            points = self.create_tentacle_points(displace_tents)

         
            name = i + 1
            # scale = 5
            # points = self.interpolate_points(points, scale)
            sweep_curve = cmds.curve(p=points, d=3, name="tent_point_curve{}".format(name))
            sweep = cmds.CreateSweepMesh()
            sweep_name = "sweepShape{}".format(i+1)

            #make tentacle here, and add it to the array of tentacles
            tentacle = Tentacle(name, name, points, sweep_curve,sweep_name)
            self.tentacles.append(tentacle)
            cmds.parent(sweep_curve, sweep_name)
            

            cmds.select(clear=True)
            
            
            cmds.setAttr("sweepMeshCreator{}.scaleProfileX".format(i + 1), self.scale)
            cmds.setAttr("sweepMeshCreator{}.taper".format(i + 1), self.taper)
            cmds.setAttr("sweepMeshCreator{}.taperCurve[0].taperCurve_Position".format(i + 1), self.taper_point)
            cmds.setAttr("sweepMeshCreator{}.taperCurve[0].taperCurve_FloatValue".format(i + 1), self.taper_val)

            ##Why was this command messing everything up?
            cmds.setAttr("sweepMeshCreator{}.interpolationPrecision".format(i + 1), 100)


            cmds.setAttr("sweepMeshCreator{}.interpolationOptimize".format(i + 1), 1)
            cmds.polySmooth("sweepShape{}".format(i + 1), mth=0, dv=2,)

            curr_sweep = "sweep{}".format(name)

            
            

            if cmds.objExists(curr_sweep):
                cmds.select(curr_sweep, replace=True)  # Select the object
                
            
            cmds.polyCloseBorder(constructionHistory=False, name='closeBorderNode')
            cmds.select(clear=True)


    def interp_tent_points(self):
        for tent in self.tentacles:
            points = tent.points
            
            points = self.interpolate_points(points)
            tent.points = points

    




    #make a helper that affects the geometry separately
    def create_bezier_curve_spline(self):
        """
        Creates a NURBS curve similar to a Bezier curve.
        """

        self.interp_tent_points()
        self.attach_joints()

    def rig_geom(self, scale):
        self.interp_tent_points(scale)
        self.update_joints()
    
    
    #This function will create joints and bind to skin
    def attach_joints(self):
        for tent in self.tentacles:
            points = tent.points
            name = tent.geometry

            #what is the need to polysmooth?
            cmds.polySmooth(name, mth=0, dv=2,)
            idx = tent.idx
            joints = self.create_joints(points,idx)

            #if a spline already exists, change the number of joints it has
            #otherwise create it

            
            # ikHandle = 'tent{}_ikHandle'.format(idx)
            # if (cmds.objExists(ikHandle)):
            #     cmds.ikHandle(ikHandle, edit = True, sj=joints[0], ee=joints[-1])

            # else:
            spline_handle, curve = self.create_ik_spline_handle(joints[0], joints[len(joints)-1],idx)
            clusters, verts = self.create_cluster(curve, idx)
            ctrls = self.create_controls(clusters, verts, idx)
            tent.ctrls = ctrls

            # sweep_name = "sweepShape{}".format(i+1)
            print("Debugging auto")
            print(name)
            print(idx)
            cmds.parent(joints[0], name)
            cmds.parent(spline_handle, name)
            cmds.parent(curve, name)

            for cont, cluster,joint in zip(ctrls, clusters, joints):
                print('This is joint size {}, this is cluster size {}, and this is ctrl size {}'.format(len(joints), len(clusters), len(ctrls)))
            
                cmds.parent(cont, name)
                cmds.parent(cluster, name)
                # cmds.setAttr(f"{joint}.visibility", False)
            
            skinCluster = cmds.skinCluster(joints, name, mi=3)[0]
    
    
    def create_bezier_curve_spline2(self):
        """
        Creates a NURBS curve similar to a Bezier curve.
        """

        tentacle_info_map = {}
        # Define control points for the curve
        for i in range(self.num_tents):
            # Randomize the angle and radius for more variation in curve starting positions
            a = random.uniform(0, 2 * math.pi)  # Random angle between 0 and 2pi
            b = random.uniform(0.5, 1.5)        # Random scale factor for radius (adjustable)

            tentacle_info_map[i] = []

            # Generate x, z coordinates for the starting points of the curve
            x = self.base_radius * math.sqrt(b) * math.cos(a)
            z = self.base_radius * math.sqrt(b) * math.sin(a)

            # Print x, z for debugging and to see the distribution
            print(f"Starting Point x: {x}, z: {z}")

            # Add the base point for the curve
            point_i = (x, 0, z)  # Base point
            points = []
            points.append(point_i)
            joints = []
            # joints.append(cmds.joint(n='tentacle{}_joint{}'.format(i + 1, 1),p=point_i))
            controllers = []
            

            # Add intermediate points to create the curve shape
            ### ADD SLIDERS FOR THESE
            for k in range(self.tent_len):
                # Randomize the vertical position (y) for variation
                ### ADD SLIDERS FOR THESE
                y = - (k+1) * 3  # Change the multiplier as needed for effect
                tentacle_x_disp = a = random.uniform(0, 2 * math.pi)
                # x += math.cos( tentacle_x_disp * self.tent_disp)
                # z += math.sin(tentacle_x_disp * self.tent_disp)

                print("This is the tentacle, and this is the point")
                new_point = (x, y, z)
                
                points.append(new_point)
                # joints.append(cmds.joint(n='tentacle{}_joint{}'.format(i + 1, k + 2),p=new_point))
                


                print("Adding point to {}th tentacle".format(i))
                tentacle_info_map[i].append(new_point)

            name = i + 1
            scale = 3
            points = self.interpolate_points(points)
            joints = self.create_joints(points,name)
            spline_handle, curve = self.create_ik_spline_handle(joints[0], joints[len(joints)-1],name)
            clusters, verts = self.create_cluster(curve, name)
            ctrls = self.create_controls(clusters, verts, name)

            cmds.select(clear=True)
            sweep_curve = cmds.curve(p=points, d=3, name="Bezier_Curve")
            sweep = cmds.CreateSweepMesh()

            # sweep = cmds.CreateSweepMesh()
            sweep_name = "sweepShape{}".format(i+1)
            cmds.parent(joints[0], sweep_name)
            cmds.parent(spline_handle, sweep_name)
            cmds.parent(curve, sweep_name)

            #print('This is joint size {}, this is cluster size {}, and this is ctrl size {}'.format(len(joints), len(clusters), len(ctrls)))
            for cont, cluster,joint in zip(ctrls, clusters, joints):
                print('This is joint size {}, this is cluster size {}, and this is ctrl size {}'.format(len(joints), len(clusters), len(ctrls)))
            
                cmds.parent(cont, sweep_name)
                cmds.parent(cluster, sweep_name)
            
            cmds.setAttr("sweepMeshCreator{}.scaleProfileX".format(i + 1), self.scale)
            cmds.setAttr("sweepMeshCreator{}.taper".format(i + 1), self.taper)
            cmds.setAttr("sweepMeshCreator{}.taperCurve[0].taperCurve_Position".format(i + 1), self.taper_point)
            cmds.setAttr("sweepMeshCreator{}.taperCurve[0].taperCurve_FloatValue".format(i + 1), self.taper_val)

            ##Why was this command messing everything up?
            cmds.setAttr("sweepMeshCreator{}.interpolationPrecision".format(i + 1), 100)


            cmds.setAttr("sweepMeshCreator{}.interpolationOptimize".format(i + 1), 1)
            cmds.polySmooth("sweepShape{}".format(i + 1), mth=0, dv=2,)



            
            # print(tentacle_info_map)
            skinCluster = cmds.skinCluster(joints, "sweepShape{}".format(i + 1), mi=3)[0]

            for cluster in clusters:
                out = cmds.listConnections( cluster[0], type="objectSet" )
                print("TESTING THE GEOMETRY AFFECTED BY")
                print(out)
                print("TESTING THE GEOMETRY AFFECTED BY")


        
        self.close_ends()
    

    def set_key_frame(self, frame):
        
        cmds.select(self.global_ctrls)

        # Set keyframes for controllers
        cmds.setKeyframe(self.global_ctrls, attribute='translateZ', t='{}'.format(frame))
        cmds.setKeyframe(self.global_ctrls, attribute='translateX', t='{}'.format(frame))
        cmds.setKeyframe(self.global_ctrls, attribute='translateY', t='{}'.format(frame))
        cmds.select(clear=True)


    def attach_to_selected_joint(self):
        anchor = cmds.ls(selection=True, type="joint")
        assert len(anchor) == 1

        for tent in self.tentacles:
            cmds.parentConstraint(anchor[0], tent.ctrls[0], mo=True, weight=1)


    def animate(self):
        # self.create_tentacle_geom(False)
        # self.attach_joints()

        # self.set_key_frame(0)
        for i in range(0 , 10):
            
            for tent in self.tentacles:
                a = random.uniform(0, 2 * math.pi)
                
                b = random.uniform(0.5, 1.5)        

                    
                tentacle_x_disp = random.uniform(-0.2, 0.2) 
                x = self.base_radius * math.sqrt(b) * math.cos(a)
                z = self.base_radius * math.sqrt(b) * math.sin(a) 

                for j,ctrl in enumerate(tent.ctrls):
                      
                    r = random.uniform(-1, 1)
                    r2 = random.uniform(-1, 1)
                    r *=  self.tent_disp
                    r2 *= self.tent_disp

                    c = random.uniform(0, math.pi/2)

                    tentacle_x_disp2 = random.uniform(-0.2, 0.2)
                    if j != 0:
                        r *=  j
                        r2 *= j
                        x = math.cos( tentacle_x_disp * self.tent_disp) * r
                        z = math.cos(tentacle_x_disp2 * self.tent_disp) * r2
                        y = math.sin(c) * random.uniform(0, 1)

                        
                    #     # Apply the new transformations
                        current_y = cmds.getAttr(f"{ctrl}.translateY")
                        # new_y = current_y - y
                        cmds.setAttr(f"{ctrl}.translateX", x)
                        cmds.setAttr(f"{ctrl}.translateY", y)
                        cmds.setAttr(f"{ctrl}.translateZ", z)

            self.set_key_frame(60 * i)

    
    def create_bezier_curve(self):
        """
        Creates a NURBS curve similar to a Bezier curve.
        """

        tentacle_info_map = {}
        # Define control points for the curve
        for i in range(self.num_tents):
            # Randomize the angle and radius for more variation in curve starting positions
            a = random.uniform(0, 2 * math.pi)  # Random angle between 0 and 2pi
            b = random.uniform(0.5, 1.5)        # Random scale factor for radius (adjustable)

            tentacle_info_map[i] = []

            # Generate x, z coordinates for the starting points of the curve
            x = self.base_radius * math.sqrt(b) * math.cos(a)
            z = self.base_radius * math.sqrt(b) * math.sin(a)

            # Print x, z for debugging and to see the distribution
            print(f"Starting Point x: {x}, z: {z}")

            # Add the base point for the curve
            point_i = (x, 0, z)  # Base point
            points = []
            points.append(point_i)
            joints = []
            joints.append(cmds.joint(n='tentacle{}_joint{}'.format(i + 1, 1),p=point_i))
            controllers = []
            

            # Add intermediate points to create the curve shape
            ### ADD SLIDERS FOR THESE
            for k in range(self.tent_len):
                # Randomize the vertical position (y) for variation
                ### ADD SLIDERS FOR THESE
                y = - (k+1) * 3  # Change the multiplier as needed for effect
                tentacle_x_disp = a = random.uniform(0, 2 * math.pi)
                x += math.cos( tentacle_x_disp * self.tent_disp)
                z += math.sin(tentacle_x_disp * self.tent_disp)

                print("This is the tentacle, and this is the point")
                new_point = (x, y, z)
                
                points.append(new_point)
                joints.append(cmds.joint(n='tentacle{}_joint{}'.format(i + 1, k + 2),p=new_point))
                


                print("Adding point to {}th tentacle".format(i))
                tentacle_info_map[i].append(new_point)

            name = i + 1
            spline_handle, curve = self.create_ik_spline_handle(joints[0], joints[len(joints)-1],name)
            clusters, verts = self.create_cluster(curve, name)
            ctrls = self.create_controls(clusters, verts, name)

            cmds.select(clear=True)
            cmds.select(curve)
            sweep = cmds.CreateSweepMesh()

            # sweep = cmds.CreateSweepMesh()
            sweep_name = "sweepShape{}".format(i+1)
            cmds.parent(joints[0], sweep_name)
            cmds.parent(spline_handle, sweep_name)
            cmds.parent(curve, sweep_name)

            #print('This is joint size {}, this is cluster size {}, and this is ctrl size {}'.format(len(joints), len(clusters), len(ctrls)))
            for cont, cluster,joint in zip(ctrls, clusters, joints):
                print('This is joint size {}, this is cluster size {}, and this is ctrl size {}'.format(len(joints), len(clusters), len(ctrls)))
            
                cmds.parent(cont, sweep_name)
                cmds.parent(cluster, sweep_name)
            
            cmds.setAttr("sweepMeshCreator{}.scaleProfileX".format(i + 1), self.scale)
            cmds.setAttr("sweepMeshCreator{}.taper".format(i + 1), self.taper)
            cmds.setAttr("sweepMeshCreator{}.taperCurve[0].taperCurve_Position".format(i + 1), self.taper_point)
            cmds.setAttr("sweepMeshCreator{}.taperCurve[0].taperCurve_FloatValue".format(i + 1), self.taper_val)

            ##Why was this command messing everything up?
            cmds.setAttr("sweepMeshCreator{}.interpolationPrecision".format(i + 1), 100)


            cmds.setAttr("sweepMeshCreator{}.interpolationOptimize".format(i + 1), 1)
            cmds.polySmooth("sweepShape{}".format(i + 1), mth=0, dv=2,)
 
            for cluster in clusters:
                out = cmds.listConnections( cluster[0], type="objectSet" )
                print("TESTING THE GEOMETRY AFFECTED BY")
                print(out)
                print("TESTING THE GEOMETRY AFFECTED BY")
        
        self.close_ends()