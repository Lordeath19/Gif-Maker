import os
import pathlib
import argparse



verbose = False



class Gif:

    #Logical Screen Descriptor
    class LSD:
        class Packed:

            # TODO: figure out what's the difference between color resolution and size of global color table

            def __init__(self, colors = [[]], sort = False):
                if len(colors) > 0:
                    # Global Color Table
                    self.gct = True
                    #Color resolution - amount of colors in the color table in powers of 2 (range : 1 - 8)
                    self.colorRes = self.get_res(colors)
                    if verbose:
                        print(f"Color table is {self.colorRes} bits")
                    self.ct = ColorTable(self.colorRes, [item for sublist in colors for item in sublist])
                else:
                    self.gct = False
                    self.colorRes = 0
                self.sort = sort
        
        def __init__(self, width, height, colors = [[]], sort = False, bgIndex = 0):
            self.width = width
            self.height = height
            self.packed = Packed(colors)
            #Sort by frequency

            # Index of background color (transparency) from the global color table
            self.backColorIndex = bgIndex

            # This is always zero because of legacy formats
            self.pixelAspectRatio = 0

        def get_res(self,colors):
            for i in xrange(1,8):
                if 2^i >= len(colors):
                    return i
            raise ValueError("Too many colors")

    # color table
    class ColorTable:
        def __init__(self, res, colors = []):
            # Total number of colors (including blanks)
            self.size = 2**(res+1)
            
            #Create an blank array to pad if there is an odd number of colors
            self.colors = [0] * (size*3 - len(colors))
            if len(colors) > 0:    
                self.colors = colors + self.colors
                if verbose:
                    print(f"Color table: {self.colors}")


    # Graphics Control Extension
    class GCE:
        
        # Packed byte containing flags and reserved bits
        class Packed:
            def __init__(self):
                self.reserved = 0
                self.disposalMethod = 0
                self.userInputFlag = False
                self.transFlag = False

        def __init__(self):
            #Constants
            self.extensionIntroducer = 21
            self.GCL = 249
            
            # Don't know what this is yet, TODO: find out what the following fields mean in the GCE
            self.byteSize = 4
            self.delayTime = 0
            self.transColorIndex = 0
            self.blcokTerminator = 0

            # The packed byte
            self.packedField = Packed()

    class ImageDesc:
        class Packed:
             def __init__(self, res = 0, colors = [[]],interlace = False, sort = False):
                # Is the image about to have a different color table
                if res > 0:
                    self.localColorFlag = True
                    self.localColorSize = res

                # Is interlacing enabled, will allow image to show before being completely loaded 
                # (it will be blurry at first and begin sharpening as the rest loads)
                self.interlaceFlag = interlace
                
                self.sortFlag = sort
                self.reserved = 0
                

        def __init__(self, colors = [[]], interlace = False, sort = false):
            #Constant seperator
            self.seperator = '\x2c'

            # Offset from the left border of the canvas
            self.imageLeft = 0
            
            # Offset from the top border of the canvas
            self.imageTop = 0
            
            # Total width of image
            self.imageWidth = 0

            # Total height of image
            self.imageHeight = 0

            self.ct = []
            self.colorRes = 0
            if len(colors) > 0:
                #Color resolution - amount of colors in the color table in powers of 2 (range : 1 - 8)
                self.colorRes = self.get_res(colors)
                if verbose:
                    print(f"local color table is {self.colorRes} bits")
                self.ct = ColorTable(self.colorRes, [item for sublist in colors for item in sublist])

            self.packed = self.Packed(self.colorRes, self.ct)


        def get_res(self,colors):
                for i in xrange(1,8):
                    if 2^i >= len(colors):
                        return i
                raise ValueError("Too many colors")

    def __init__(self, fileName):
        
        # If the file exists, just overwrite it
        if os.path.exists(fileName):
            if verbose:
                print("Output file exists, overwriting")

        # If the file doesn't exist, try to create all leading directories to said file before creating    
        else:
            if verbose:
                print("Creating parent folders, if they don't exist")
            pathlib.Path(os.path.dirname(fileName)).mkdir(parents=True, exist_ok=True)

        self.gifFile = open(fileName,'wb')
        
        # Signature of gif
        self.signature = "GIF"
        
        # Version of gif (87a is used more so that's the default)
        self.version = "87a"
        
        self.lsd = self.LSD()

        # No need for GCE for now as it's optional, TODO: Decide what to do with this
        # self.gce = self.GCE()
        
        self.ImageDesc = self.ImageDesc()
        
        #Dimensions
        self.totalHeight = 0
        self.totalWidth = 0



        self.gifFile.close()
    
    def add_image(self,imageSource):
        if not os.path.exists(fileName):
            if verbose:
                print(f"Image: {imageSource} doesn't exists, skipping")
            return
        
        
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    parser.add_argument("images", help = "Full path to source images", nargs='*')
    args = parser.parse_args()
    verbose = args.verbose
    gifFile = Gif("Output.gif")

    for i in args.images:
        gifFile.add_image(i)