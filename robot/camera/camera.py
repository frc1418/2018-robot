#!/usr/bin/env python3

import cscore as cs


def main():
    main_camera = cs.UsbCamera('Main', 0)
    main_camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 160, 120, 30)

    main_server = cs.MjpegServer('httpserver', 1181)
    main_server.setSource(main_camera)

    intake_camera = cs.UsbCamera('Intake', 1)
    intake_camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 160, 120, 30)

    intake_server = cs.MjpegServer('httpserver', 1182)
    intake_server.setSource(intake_camera)

    # Wait indefinitely
    input('Press enter to terminate.')


if __name__ == '__main__':
    main()
