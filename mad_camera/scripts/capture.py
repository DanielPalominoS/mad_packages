import arducam_mipicamera as arducam
import v4l2 #sudo pip install v4l2
import time

def set_controls(camera):
    try:
        print("Reset the focus...")
        camera.reset_control(v4l2.V4L2_CID_FOCUS_ABSOLUTE)
	camera.set_control( v4l2.V4L2_CID_EXPOSURE, 0x00F0 )
    except Exception as e:
        print(e)
        print("The camera may not support this control.")

    try:
        print("Enable Auto Exposure...")
        camera.software_auto_exposure( enable = True )
        print("Enable Auto White Balance...")
        camera.software_auto_white_balance( enable = True )
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        camera = arducam.mipi_camera()
        print("Open camera...")
        camera.init_camera()
        print("Setting the resolution...")
        fmt = camera.set_resolution( 4672,3496 )
        print("Current resolution is {}".format(fmt))
        # print("Start preview...")
        # camera.start_preview(fullscreen = False, window = (0, 0, 1280, 720))
        set_controls(camera)
        time.sleep(1)
        frame = camera.capture(encoding = 'jpeg',quality=100 )
        frame.as_array.tofile("{}x{}.jpg".format(fmt[0],fmt[1]))

        # Release memory
        del frame
        # print("Stop preview...")
        # camera.stop_preview()
        print("Close camera...")
        camera.close_camera()
    except Exception as e:
        print(e)
