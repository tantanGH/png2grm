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

### 使用例

- 縦640ピクセル、横640ピクセルの1:1PNG画像をX68000 512x512x65536色モードでできるだけアスペクト比を維持しながら表示させたい場合

<img src='images/sample1.png'/>

横384ピクセル、縦512ピクセルで出力する。これより小さいサイズにする場合はこの比率(3:4)を維持する。

        png2grm -w 384 -h 512 sample1.png sample1.grm

X68000側で MicroPython を使って表示する例

        import x68k

        x68k.crtmod(12,True)

        gvram = x68k.GVRam()
        with open("sample1.grm", "rb") as f:
          for y in range(0, 512, 64):
            grm_data = f.read(2 * 384 * 64)
            gvram.put(0, y, 383, y + 63, grm_data)

<img src='images/sample1x.png'/>

注意：X68000の512x512モードのアスペクト比は3:2と言われているが、これはブラウン管(CRT)では周辺の歪みを避けるためにオーバースキャン気味に設定されていたためと思われる。


- 縦768ピクセル、横512ピクセルの3:2PNG画像をX68000 512x512x65536色モードでできるだけアスペクト比を維持しながら表示させたい場合

<img src='images/sample2.png'/>

横512ピクセル、縦456ピクセルで出力する。これより小さいサイズにする場合はこの比率(約8:7)を維持する。

        png2grm -w 512 -h 456 sample2.png sample2.grm

X68000側で MicroPython を使って表示する例

        import x68k

        x68k.crtmod(12,True)

        gvram = x68k.GVRam()
        with open("sample2.grm", "rb") as f:
          for y in range(0, 456, 8):
            grm_data = f.read(2 * 512 * 8)
            gvram.put(0, y, 511, y + 7, grm_data)

もし高さを16の倍数として扱い易くしたい場合は縦464ピクセルでもほぼ問題ない。

        png2grm -w 512 -h 464 sample2.png sample2.grm

X68000側で MicroPython を使って表示する例

        import x68k

        x68k.crtmod(12,True)

        gvram = x68k.GVRam()
        with open("sample2.grm", "rb") as f:
          for y in range(0, 464, 16):
            grm_data = f.read(2 * 512 * 16)
            gvram.put(0, y, 511, y + 15, grm_data)


<img src='images/sample2x.png'/>

---