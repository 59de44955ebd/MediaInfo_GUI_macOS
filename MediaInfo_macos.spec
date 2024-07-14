# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['_bootlocale'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MediaInfo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['MediaInfo.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='MediaInfo',
)
app = BUNDLE(
    coll,
    name='MediaInfo.app',
    icon='MediaInfo.icns',
    bundle_identifier=None,
    info_plist={
        'CFBundleShortVersionString': '0.1.0',
        'CFBundleDocumentTypes': [
            {
                'LSItemContentTypes': ['public.data'],
                'CFBundleTypeRole': 'Viewer'
            }
        ]
    },
)

