import pymel.core
import os

'''
Annie Hirata
This module contains functions to apply one or more animations to a
given character
'''

def _create_namespace_from_file(file_path):
    if not os.path.exists(file_path):
        pymel.core.error('File does not exist: {}'.format(file_path))
        return
    
    file_name_full = os.path.split(file_path)[1]
    file_name = os.path.splitext(file_name_full)[0]
    return file_name
    

def _create_reference(file_path, ns):
    if not os.path.exists(file_path):
        pymel.core.error('File does not exist: {}'.format(file_path))
        return

    return pymel.core.system.createReference(file_path, ns=ns)


def _connect_bones(src_list, dest_ns):
    # connect any bones with the same name in the src and dest joint lists
    for src_bone in src_list:
        bone = src_bone.split(':')[1]

        try:
            dest_bone = pymel.core.PyNode('{}:{}'.format(dest_ns, bone))
            pymel.core.animation.parentConstraint(src_bone, dest_bone, mo=True)
        except pymel.core.MayaNodeError:
            pass


def _bake_animation(obj):
    start_time = pymel.core.playbackOptions(q=True, min=True)
    end_time = pymel.core.playbackOptions(q=True, max=True)     

    pymel.core.select(cl=True)
    pymel.core.select(obj)
    pymel.core.bakeResults(simulation = True,
                        time = (start_time, end_time),
                        sampleBy = 1,
                        oversamplingRate= 1,
                        disableImplicitControl = True,
                        preserveOutsideKeys = True,
                        sparseAnimCurveBake = False,
                        removeBakedAnimFromLayer = False,
                        bakeOnOverrideLayer = False,
                        minimizeRotation = True,
                        controlPoints = False,
                        shape = True)


def apply_animation(anim_file, char_file, save_dir):
    '''
    Apply an animation to a character and save.
    Parameters
        anim_file: str
            The path to the directory containing all the animations to apply
        char_file: str
            The path to the character file (.ma or .mb)
        save_dir: str
            The directory to save the applied animation file to
    '''
    # Replace any backslashes
    anim_file = anim_file.replace('\\', '/')
    char_file = char_file.replace('\\', '/')
    save_dir = save_dir.replace('\\', '/')

    # Create new scene
    pymel.core.newFile(f=1)
    
    # Create namespaces
    char_ns = _create_namespace_from_file(char_file)
    anim_ns = _create_namespace_from_file(anim_file)
    
    # Bring in the character
    char_ref = _create_reference(char_file, char_ns)
    
    # Bring in the animation
    anim_ref = _create_reference(anim_file, anim_ns)

    # Frame the animation
    pymel.core.viewFit(ns = anim_ns)
    
    # Get list of joints for the animation
    anim_joints = pymel.core.ls(anim_ref.nodes(), type='joint')
    char_joints = pymel.core.ls(char_ref.nodes(), type='joint')
    
    # Set the current framerate to match the framerate of the referenced animation
    first_key = pymel.core.findKeyframe(anim_joints[0], which='first')
    pymel.core.currentTime(first_key)
    
    # Map the joints of the animation onto the character
    _connect_bones(anim_joints, char_ns)
    
    # Bake the animation bones to the character bones
    _bake_animation(char_joints)
    
    # Remove the reference
    anim_ref.remove()

    # If the save directory doesnt exist, create it
    if not os.path.exists(save_dir):
        print("Creating save directory: {}".format(save_dir))
        os.makedirs(save_dir)

    # Save the file
    anim_file_name = os.path.split(anim_file)[1]
    renamed_file = os.path.join(save_dir, '{}_{}'.format(char_ns, anim_file_name))
    
    pymel.core.system.renameFile(renamed_file)
    pymel.core.system.saveFile(save=True, f=True)


def batch_animations(char_file, anim_dir, save_dir, progress_bar = None):
    '''
    Apply multiple animations in a directory to a character and save.
    Parameters
        char_file: str
            The path to the character file (.ma or .mb)
        anim_dir: str
            The path to the directory containing all the animations to apply
        save_dir: str
            The directory to save the applied animation files to
        progress_bar: BatchAnimationsUI.ProgressDialog, optional
            The progress dialog shown during batching
    '''

    # File/directory error checking
    if not os.path.exists(char_file):
        print("Character file does not exist: {}".format(char_file))

    if not os.path.exists(anim_dir):
        print("Animation directory does not exist: {}".format(anim_dir))

    # Check that the save_dir exists, if not create it
    if not os.path.exists(save_dir):
        print("Creating save directory: {}".format(save_dir))
        os.makedirs(save_dir)

    # Get all files in the animations directory that have extension .ma or .mb
    anim_files = [os.path.join(anim_dir, f) for f in os.listdir(anim_dir) if os.path.exists(os.path.join(anim_dir, f)) and (f.endswith('.ma') or f.endswith('.mb'))]

    # If there is a progress bar passed, set the maximum
    if progress_bar:
        progress_bar.set_max_progress(len(anim_files))

    # For animation file in animation directory, apply the animation to the character
    for i, anim_file in enumerate(anim_files, 1):
        if progress_bar:
            progress_bar.set_label_text("Processing file: {}".format(anim_file))

        print("Processing file: {}".format(anim_file))
        apply_animation(anim_file, char_file, save_dir)

        # Update progress bar
        if progress_bar:
            progress_bar.set_progress_value(i)

    