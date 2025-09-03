import cv2
from cv2_enumerate_cameras import enumerate_cameras

def list_cameras_with_names():
    """
    Lists all connected cameras with their system names and indices.

    This function uses a specialized library to query the operating system
    for all available video capture devices. It returns a list of dictionaries,
    where each dictionary contains information about a camera.

    Returns:
        list: A list of dictionaries, where each dict has 'index' and 'name'.
    """
    camera_list = []
    
    # Use the enumerate_cameras function from the library to get detailed info
    # for each connected camera. The function returns a list of objects.
    try:
        camera_info_list = enumerate_cameras()
    except Exception as e:
        print(f"Error enumerating cameras: {e}")
        return []

    if not camera_info_list:
        return []
    
    # Iterate through the returned objects and extract the name and index.
    for camera_info in camera_info_list:
        camera_list.append({
            'index': camera_info.index,
            'name': camera_info.name
        })
        
    return camera_list

# This is an example of how to use the function
if __name__ == "__main__":
    print("Searching for connected cameras...")
    connected_cams = list_cameras_with_names()
    
    if connected_cams:
        print("\nFound the following cameras:")
        for cam in connected_cams:
            print(f"  - Index {cam['index']}: '{cam['name']}'")
    else:
        print("\nNo cameras were found.")