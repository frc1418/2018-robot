#!/usr/bin/env python3

import cscore


def main():
    cs = cscore.CameraServer.getInstance()
    cs.enableLogging()

    cs.startAutomaticCapture(dev=0)
    cs.startAutomaticCapture(dev=1)

    cs.waitForever()


if __name__ == '__main__':
    main()
