# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['indlan.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy', 'sklearn', 'scikit-learn', 'tensorflow', 'keras', 'torch', 'torchvision', 'transformers', 'spacy', 'nltk', 'plotly', 'openpyxl', 'xlsxwriter', 'joblib', 'PIL', 'pillow', 'cv2', 'cryptography', 'charset_normalizer', 'urllib3', 'requests', 'certifi', 'IPython', 'pytest', 'setuptools', 'wheel', 'pip', 'pycparser', 'cffi', 'pydantic', 'pydantic_core', 'rich', 'typer', 'click'],
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
    name='IndLan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['indlan_icon.ico'],
)
