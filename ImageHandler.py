import os

class ImageHandler:

  ImageMagick = None
  tempFile = None
  
  colors = [['#000000','#010101'],                     # black
            ['#990000','#980000','#970000'],           # red
            ['#ffcc00','#ffcb00','#fecb00','#fdca00'], # yellow
            ['#33b100','#34b000','#34af00','#33b000']] # green

  ##############################################################################
  # sets up Selenium
  def __init__(self, ImageMagick, tempFile):
    self.ImageMagick = ImageMagick
    self.tempFile = tempFile

  ##############################################################################
  # processes a frame, including color analysis and annotation
  def processImage(self, inFile, outFile, currentTime):
    base = self.ImageMagick + ' '
    print('processing %s...' % inFile)
    # crop first
    cmd = base + inFile + ' -crop 900x900+700+60 %s' % self.tempFile
    os.system(cmd)

    tail = '-format %c histogram:info:'

    # analyze colors
    counts = []
    total = 0
    for color in self.colors:
      cmd = base + self.tempFile + ' -fill %s ' % color[0]
      for variant in color[1:]:
        cmd += '-opaque %s ' % variant
      cmd += '-fill #ffffff +opaque %s ' % color[0] + tail
      p = os.popen(cmd)
      line = p.readline()
      count = 0
      if 'white' not in line:
        count = int(line.split(':')[0])
      p.close()
      counts.append(count)
      total += count

    # draw boxes
    width = 105
    offset = 10
    x = offset
    cmd = base + self.tempFile + ' -fill #000000b0 -draw "rectangle %d,10 %d,40" ' % (offset, offset + width)
    for i in range(len(self.colors)):
      count = counts[i]
      portion = int(round(float(count) / float(total) * width))
      #print(portion)

      # handle rounding issues
      if (x + portion == offset + width + 1):
        portion -= 1
      elif (x + portion == offset + width - 1):
        portion += 1

      cmd += '-fill %s -draw "rectangle %d,41 %d,43" ' % (self.colors[i][0], x, x + portion)
      x += portion

    # print time
    hour = int(currentTime[0])
    end = 'am'
    if hour == 0:
      hour = 12
    elif hour >= 12:
      end = 'pm'
      if hour > 12:
        hour -= 12
    text = "%02d:%s %s" % (hour, currentTime[1], end)
    cmd += ' -pointsize 24 -font Arial -gravity center -fill white -annotate -196-454 "%s" ' % text

    # save output
    cmd += '%s' % (outFile)
    os.system(cmd)
    print('frame processed.')