import os
import subprocess
import sys
import Cocoa
from PyObjCTools import AppHelper

IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    BIN = os.path.join(os.path.dirname(sys.executable), '..', 'Resources', 'mediainfo')
else:
    BIN = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'mediainfo')


class App():

    def __init__(self):
        app = self

        class MyScrollView(Cocoa.NSScrollView):
            def draggingEntered_(self, sender):
                return True
            def performDragOperation_(self, sender):
                pb_objects = sender.draggingPasteboard().readObjectsForClasses_options_([Cocoa.NSURL], None)
                app.load_file(pb_objects[0].path())
                return True

        class MyAppDelegate(Cocoa.NSObject):
            def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
                return True
            def applicationShouldTerminate_(self, sender):
                return Cocoa.NSTerminateNow
            def application_openFile_(self, application, filename):
                if IS_FROZEN:
                    app.load_file(filename)
                    return True
                return False

        Cocoa.NSApplication.sharedApplication()
        Cocoa.NSApp().setDelegate_(MyAppDelegate.alloc().init())

        self.win = Cocoa.NSWindow.alloc()
        self.win.initWithContentRect_styleMask_backing_defer_(((0.0, 0.0), (640, 900)),
                Cocoa.NSTitledWindowMask | Cocoa.NSClosableWindowMask | Cocoa.NSResizableWindowMask | Cocoa.NSMiniaturizableWindowMask,
                2, 0)
        self.win.setLevel_(Cocoa.NSNormalWindowLevel)
        self.win.center()

        self.text_view  = Cocoa.NSTextView.alloc().init()
        self.text_view.setAutoresizingMask_(Cocoa.NSViewHeightSizable | Cocoa.NSViewWidthSizable)
        self.text_view.setEditable_(False)
        self.text_view.setFont_(Cocoa.NSFont.userFixedPitchFontOfSize_(12))
        self.text_view.setString_('Drag media files either into this window or on the application\'s Dock icon.')

        scroll_view = MyScrollView.alloc().init()
        scroll_view.setHasVerticalScroller_(True)
        scroll_view.registerForDraggedTypes_([Cocoa.NSPasteboardTypeFileURL])
        scroll_view.setDocumentView_(self.text_view)

        self.win.setContentView_(scroll_view)
        self.win.orderFrontRegardless()

        if not IS_FROZEN and len(sys.argv) > 1:
            self.load_file(sys.argv[1])

    def load_file(self, filename):
        self.win.setTitle_(f"MediaInfo - {filename}")
        infos = subprocess.run([BIN, filename],
            capture_output=True, shell=False).stdout.decode()
        self.text_view.setString_(infos)
        self.win.orderFrontRegardless()


if __name__ == "__main__":
    App()
    AppHelper.runEventLoop()
