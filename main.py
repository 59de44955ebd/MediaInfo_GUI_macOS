import os
import subprocess
import sys
import objc
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
        self.timer = None
        self.files = []

        class MyScrollView(Cocoa.NSScrollView):
            def draggingEntered_(self, sender):
                return True
            def performDragOperation_(self, sender):
                pb_objects = sender.draggingPasteboard().readObjectsForClasses_options_([Cocoa.NSURL], None)
                app.load_files([po.path() for po in pb_objects])
                return True

        class MyAppDelegate(Cocoa.NSObject):
            def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
                return True
            def applicationShouldTerminate_(self, sender):
                return Cocoa.NSTerminateNow
            def application_openFiles_(self, application, filenames):
                if IS_FROZEN:
                    app.files.extend(filenames)
                    if app.timer is None:
                        app.timer = Cocoa.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                                .25, self, objc.selector(self._load, signature=b'v@:'), None, False)
                Cocoa.NSApp().replyToOpenOrPrint_(Cocoa.NSApplicationDelegateReplySuccess)
            def _load(self):
                files = list(app.files)
                app.timer = None
                app.files = []
                app.load_files(files)

        Cocoa.NSApplication.sharedApplication()
        Cocoa.NSApp().setDelegate_(MyAppDelegate.alloc().init())

        self.win = Cocoa.NSWindow.alloc()
        self.win.initWithContentRect_styleMask_backing_defer_(((0.0, 0.0), (640, 900)),
                Cocoa.NSTitledWindowMask | Cocoa.NSClosableWindowMask | Cocoa.NSResizableWindowMask | Cocoa.NSMiniaturizableWindowMask,
                Cocoa.NSBackingStoreBuffered, False)
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
            self.load_files(sys.argv[1:])

    def load_files(self, filenames):
        cnt = len(filenames)
        self.win.setTitle_(f"MediaInfo - {cnt} files" if cnt > 1 else f"MediaInfo - {filenames[0]}")
        self.text_view.setString_(subprocess.run([BIN] + filenames, capture_output=True).stdout.decode())


if __name__ == "__main__":
    App()
    AppHelper.runEventLoop()
