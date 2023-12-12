import numpy as np
import time
import math
import configparser
import os
#输入：.npy .hdr .obj .tga
#输出：渲染图片文件夹


def createDir(dirpath):
    import os
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    return dirpath

def renderMultiInput(shape_set,hdri_set,camera_poses_file,texture_name_set):
    
    project_name = 'DiLiGenT_RT_proj'
    base_dir = r'C:\Users\ysy\Desktop\RenderWithBlender'

    output_base_dir = os.path.join(base_dir, 'result')
    ini_basic_path = os.path.join(base_dir, 'config/templete.ini')
    ini_used_path = os.path.join(base_dir, 'config/current.ini')
    render_script_path = 'render_engine.py'

    para_dir = os.path.join(base_dir, 'supp')
    print(camera_poses_file)
    camera_poses_name = camera_poses_file

    ini = configparser.ConfigParser()
    ini.optionxform = str
    ini.read(ini_basic_path)
    print(ini_basic_path)

    ini['settings']['working_dir'] = para_dir
    ini['settings']['out_dir'] = output_base_dir
    createDir(output_base_dir)
    ini['light']['energy'] = "20"

    # todo add area light texture path
    area_light_textures = np.loadtxt(os.path.join(para_dir, ini['light']['texture_paths_csv']), delimiter=',',dtype=str)
    ini['light']['amount'] = str(len(area_light_textures))


    for shape_name in shape_set:
        for hdri_name in hdri_set:
            for texture_name in texture_name_set:
                ini['settings']['object_file'] = 'obj_data/{}.obj'.format(shape_name)
                ini['object']['enable_rendering_by_degree'] = "False"
                #load texture
                ini['camera']['camera_poses_path'] = camera_poses_name
                ini['rendering']['use_hdri'] = hdri_name
                # ini['rendering']['use_hdri'] = "None"
                ini['pbr_material']['color_texture'] = texture_name+"/"+texture_name+"_baseColor.tga"
                ini['pbr_material']['metallic_texture']= texture_name+"/"+texture_name+"_metallic.tga"
                ini['pbr_material']['specular_texture']= texture_name+"/"+texture_name+"_specular.tga"
                ini['pbr_material']['roughness_texture']= texture_name+"/"+texture_name+"_roughness.tga"
                ini['pbr_material']['normal_texture']= texture_name+"/"+texture_name+"_normal.png"

                # np.savetxt(camera_pose_file_name_i, camera_poses_path, delimiter=',')
                filename_str = '{}_{}_{}'.format(shape_name,hdri_name,texture_name)
                ini['settings']['filename_str'] = filename_str
                with open(ini_used_path, 'w') as f:
                    ini.write(f)

                os.system("blender -b -P {} {} ".format(render_script_path, ini_used_path))

if __name__ =='__main__':
    shape_set = ['18']
    hdri_set = ["hdri-54.hdr"]
    camera_poses_file = "NERO_camera.npy"
    texture_name_set = ["Plastic-carbon_fiber_plain_weave"]
    
    renderMultiInput(shape_set,hdri_set,camera_poses_file,texture_name_set)

