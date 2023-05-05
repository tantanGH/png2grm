import argparse

from PIL import Image

def convert_png_to_gvram(png_file, out_file, size):

  # open raw image
  raw_image = Image.open(png_file).convert('RGB').resize(size)
  raw_image_bytes = raw_image.tobytes()

  # convert to x68k GVRAM format
  out_bytes = bytearray()
  for i,b in enumerate(raw_image_bytes):
    if ( i % 3 ) == 2:
      r = raw_image_bytes [ i - 2 ]
      g = raw_image_bytes [ i - 1 ]
      b = raw_image_bytes [ i - 0 ]
      rgb555 = ((g>>3)<<11) | ((r>>3)<<6) | ((b>>3)<<1) | 0
      if rgb555 != 0:
        rgb555 += 1
      out_bytes.extend(rgb555.to_bytes(2, 'big'))

  # output to file
  with open(out_file, "wb") as f:
    f.write(out_bytes)

def convert_png_to_gvram256(png_file, out_file, size):

  # open raw image
  raw_image = Image.open(png_file).convert('RGB').resize(size) \
                   .quantize(colors=256, method=1, kmeans=100, dither=1)

  raw_image_bytes = raw_image.tobytes()
  raw_image_palette = raw_image.getpalette()

  # output palettes
  out_bytes = bytearray()
  for i in range(256 * 3):
    if ( i % 3 ) == 2:
      r = raw_image_palette[ i - 2 ]
      g = raw_image_palette[ i - 1 ]
      b = raw_image_palette[ i - 0 ]
      rgb555 = ((g>>3)<<11) | ((r>>3)<<6) | ((b>>3)<<1) | 0
      if rgb555 != 0:
        rgb555 += 1
      out_bytes.extend(rgb555.to_bytes(2, 'big'))

  # output index colors
  out_bytes.extend(raw_image_bytes)

  # output to file
  with open(out_file, "wb") as f:
    f.write(out_bytes)

def convert_png_to_gvram16(png_file, out_file, size):

  # open raw image
  raw_image = Image.open(png_file).convert('RGB').resize(size) \
                   .quantize(colors=16, method=1, kmeans=100, dither=1)

  raw_image_bytes = raw_image.tobytes()
  raw_image_palette = raw_image.getpalette()

  # output palettes
  out_bytes = bytearray()
  for i in range(16 * 3):
    if ( i % 3 ) == 2:
      r = raw_image_palette[ i - 2 ]
      g = raw_image_palette[ i - 1 ]
      b = raw_image_palette[ i - 0 ]
      rgb555 = ((g>>3)<<11) | ((r>>3)<<6) | ((b>>3)<<1) | 0
      if rgb555 != 0:
        rgb555 += 1
      out_bytes.extend(rgb555.to_bytes(2, 'big'))

  # output index colors
  for i,b in enumerate(raw_image_bytes):
    if ( i % 2 ) == 1:
      l = raw_image_bytes [ i - 1 ]
      r = raw_image_bytes [ i - 0 ]
      out_bytes.append(((l << 4) | r) & 0xff)

  # output to file
  with open(out_file, "wb") as f:
    f.write(out_bytes)

def convert_png_to_tvram(png_file, out_file, size):

  # open raw image
  raw_image = Image.open(png_file).convert('RGB').resize(size)
  raw_image_bytes = raw_image.tobytes()

  # convert to x68k TVRAM format
  out_bytes = bytearray()
  out_bytes.extend(size[0].to_bytes(2, 'big'))
  out_bytes.extend(size[1].to_bytes(2, 'big'))
  p = 0
  for i,b in enumerate(raw_image_bytes):
    if ( i % 3 ) == 2:
      r = raw_image_bytes [ i - 2 ]
      g = raw_image_bytes [ i - 1 ]
      b = raw_image_bytes [ i - 0 ]
      if ( r + g + b ) > ( 128 + 128 + 128 ):
        p = ( p << 1 ) | 1
      else:
        p = ( p << 1 )
      if ( i % ( 16 * 3 )) == 16 * 3 - 1:
        out_bytes.extend(p.to_bytes(2, 'big'))
        p = 0

  # output to file
  with open(out_file, "wb") as f:
    f.write(out_bytes)

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("infile", help="input PNG file")
    parser.add_argument("outfile", help="output GVRAM file")
    parser.add_argument("-x","--width", help="out width (default:512)", type=int, default=512)
    parser.add_argument("-y","--height", help="out height (default:512)", type=int, default=512)
    parser.add_argument("-c","--colors", help="output colors (65536/256/16, default:65536)", type=int, choices=[65536, 256, 16], default=65536)
    parser.add_argument("-t","--tvram", help="output in text vram mono format", action='store_true', default=False)

    args = parser.parse_args()

    if args.tvram:
      convert_png_to_tvram(args.infile, args.outfile, ( args.width, args.height ))
    elif args.colors == 16:
      convert_png_to_gvram16(args.infile, args.outfile, ( args.width, args.height ))
    elif args.colors == 256:
      convert_png_to_gvram256(args.infile, args.outfile, ( args.width, args.height ))
    else:
      convert_png_to_gvram(args.infile, args.outfile, ( args.width, args.height ))

if __name__ == "__main__":
    main()
