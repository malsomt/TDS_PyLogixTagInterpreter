# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\tyler.malsom\\PycharmProjects\\TDS_PyLogixTagInterpreter'],
    binaries=[],
    datas=[('C:\\Users\\tyler.malsom\\PycharmProjects\\TDS_PyLogixTagInterpreter\\icon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TDS_MessageTool_v1.4',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\tyler.malsom\\PycharmProjects\\TDS_PyLogixTagInterpreter\\icon.ico'],
)
