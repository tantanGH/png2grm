# png2grm
PNG to 16bit X68k GVRAM format converter

---

### Install

    pip install git+https://github.com/tantanGH/png2grm.git

参考：[Windowsユーザ向けPython導入ガイド](https://github.com/tantanGH/distribution/blob/main/windows_python_for_x68k.md)

---

### Usage

    png2grm [options] <input-png-file> <output-grm-file>

Input PNG file can be RGB PNG or RGBA transparent PNG either.

    options:
        -x [width]       ... 出力横サイズ
        -y [height]      ... 出力縦サイズ

---