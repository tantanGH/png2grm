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
      out_bytes.append(rgb555.to_bytes(2, 'big'))

  # output to file
  with open(out_file, "wb") as f:
    f.write(out_bytes)

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("infile", help="input PNG file")
    parser.add_argument("outfile", help="output GVRAM file")
    parser.add_argument("-x","--width", help="out width (default:512)", type=int, default=512)
    parser.add_argument("-y","--height", help="out height (default:512)", type=int, default=512)

    args = parser.parse_args()

    convert_png_to_gvram(args.infile, args.outfile, ( args.width, args.height ))

if __name__ == "__main__":
    main()
