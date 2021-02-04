# -*- mode: python ; coding: utf-8 -*-
import os
import importlib

block_cipher = None

easy_ocr_dir = os.path.dirname(importlib.import_module('easyocr').__file__)

a = Analysis(['main.py'],
             pathex=['C:\\Users\\beard\\OneDrive\\Documents\\GitHub\\climber'],
             binaries=[],
             datas=[('drivers/*.exe', 'drivers/'),
                    ('blank.jpg', '.'),
                    ('test_data*', '.'),
                    ('test_scan*', '.'),
                    (os.path.expanduser('~/.EasyOCR/model'), 'model'),
                    (os.path.join(easy_ocr_dir, 'dict', 'en*'), os.path.join('easyocr', 'dict')),
                    (os.path.join(easy_ocr_dir, 'character', 'en*'), os.path.join('easyocr', 'character')),
                    ],
             hiddenimports=['easyocr.model.model'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='climber',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='climber')
