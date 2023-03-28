# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:\\Users\\ashew\\OneDrive\\Desktop\\PANTHIUM_THINGS\\panthium-core-main\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\ashew\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\customtkinter', 'customtkinter'), ('aimlogoDARK.png', '.'), ('aimlogoLIGHT.png', '.'), ('miscaimLIGHT.png', '.'), ('miscaimDARK.png', '.'), ('visualsLIGHT.png', '.'), ('visualsDARK.png', '.'), ('generallogoLIGHT.png', '.'), ('generallogoDARK.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
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
)
