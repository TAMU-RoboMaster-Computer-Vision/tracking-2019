# Imports the MOSSE tracker from OpenCV
from cv2 import TrackerMOSSE_create


# Creates the MOSSE tracker object
tracker = TrackerMOSSE_create()


# Starts tracking the object surrounded by the bounding box in the image
def init(image, bbox, video = []):

    # Attempts to start the tracker
    ok = tracker.init(image, bbox)

    # Checks if the initialization was successful
    if ok:

        # Goes through each frame that occurred since the first image was found
        for frame in video:
            ok = update(frame)

    # Returns the tracker's status
    return ok


print(f'The cat is {update()}', end='\r')

# Updates the location of the object
def update(image):

    # Attempts to update the object's location
    ok, location = tracker.update(image)

    # Returns the location if the location was updated
    if ok:
        return location
        # return (location[0] + location[2] / 2, location[1] + location[3] / 2)

    # Returns false the updating the location fails
    else:
        return False