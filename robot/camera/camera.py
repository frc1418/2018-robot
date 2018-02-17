#!/usr/bin/env python3

from cscore import CameraServer, UsbCamera


def main():
    cs = CameraServer.getInstance()
    cs.enableLogging()

    main_camera = UsbCamera('Main Camera', 0)
    main_camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 160, 120, 30)
    main_camera.setExposureAuto()
    main_camera.getProperty('backlight_compensation').set(5)

    main_server = cs.MjpegServer('httpserver', 1181)
    main_server.setSource(main_camera)

    intake_camera = UsbCamera('Intake Camera', 1)
    intake_camera.setVideoMode(cs.VideoMode.PixelFormat.kMJPEG, 160, 120, 30)
    intake_camera.setExposureAuto()
    intake_camera.getProperty('backlight_compensation').set(5)

    intake_server = cs.MjpegServer('httpserver', 1182)
    intake_server.setSource(intake_camera)

    cs.waitForever()


if __name__ == '__main__':
    main()
