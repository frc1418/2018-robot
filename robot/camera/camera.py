#!/usr/bin/env python3

import cscore


class Sight:
    def __init__(self):
        self.main_camera = cscore.UsbCamera('Main Camera', 0)
        self.main_camera.setVideoMode(cscore.VideoMode.PixelFormat.kMJPEG, 160, 120, 30)
        self.main_camera.setExposureAuto()
        self.main_camera.getProperty('backlight_compensation').set(5)

        self.main_server = cscore.MjpegServer('httpserver', 1181)
        self.main_server.setSource(self.main_camera)

        self.intake_camera = cscore.UsbCamera('Intake Camera', 1)
        self.intake_camera.setVideoMode(cscore.VideoMode.PixelFormat.kMJPEG, 160, 120, 30)
        self.intake_camera.setExposureAuto()
        self.intake_camera.getProperty('backlight_compensation').set(5)

        self.intake_server = cscore.MjpegServer('httpserver', 1182)
        self.intake_server.setSource(self.intake_camera)


def main():
    Sight().process()


if __name__ == '__main__':
    main()
