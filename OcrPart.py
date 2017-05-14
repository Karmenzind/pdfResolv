# coding: utf-8

import os
import pyocr
import pyocr.builders
import PyPDF2
from PIL import Image
try:
    from wand.image import Image as wandImage
    import io
    image_module = 'wand'
except:
    print "from wand.image import Image FAILED"
    import PythonMagick
    image_module = 'magick'

Image.MAX_IMAGE_PIXELS = None

class ManImage(object):
    """ 
    Manipulate Image Object 
    """

    def __init__(self, i_file, o_dire):
        """ 
        init args 
        :param i_file: (str) input pdf file's path (eg: "/home/file.pdf") 
        :param o_dire: (str) output image directory (eg: "/home/") 
        """
        self.i_file = i_file
        self.o_dire = o_dire
        if image_module == 'magick':
            with file(self.i_file, "rb") as tmp_f:
                self.pages = PyPDF2.PdfFileReader(tmp_f).getNumPages()
            print('Totally get ***{0:^4}*** pages from "{1.i_file}", playpdf start......'.format(self.pages, self))
        else:
            with wandImage(filename=i_file, resolution=300) as tmp_f:
                self.image_jpeg = tmp_f.convert('jpeg')

    def fetch_pic_txt(self, pageidx, ds=1024):
        """ 
        split pdf file 
        :param ds: (int) set ds = 1024 ~= 1MB output under my test 
        :return: splited PNG image file 
        """
        if image_module == 'magick':
            image = PythonMagick.Image()
            image.density(str(ds))
            image.read(str(self.i_file + '[%s]' % pageidx))
            image.magick("PNG")
            pic_path = os.path.abspath(os.path.join(self.o_dire, "tmppicforpdf_{}.png".format(pageidx+1)))
            image.write(pic_path)
            with Image.open(pic_path) as img_f:
                txt = recogniz(img_f)
        else:
            with wandImage(image=self.image_jpeg.sequence[pageidx]) as img_page:
                img = img_page.make_blob('jpeg')
                with Image.open(io.BytesIO(img)) as img_f:
                    txt = recogniz(img_f)
        print "Got OCR result from page", pageidx+1
        return txt

tool = pyocr.get_available_tools()[0]


def recogniz(img_f):
    txt = tool.image_to_string(img_f,
                               lang=u'eng',
                               builder=pyocr.builders.TextBuilder())
    return txt

if __name__ == '__main__':
    recogniz(r'C:\Users\Karmenzind\Desktop\20170510103757.png')