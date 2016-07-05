import os
import ftplib
from PIL import Image

def resize_and_copy_to_cesta_ftp(filename,source,userId):
    #properties
    ftp = ftplib.FTP('cestasnp.sk')
    ftp.login("cestasnp.sk",'kockovo1256')
    ftp.cwd('/web/images/stories/Ostatne/sledovanie_upload')
    #image size and quality of output if resize is needed
    out_image_size = 1024
    out_image_quality = 80
    
    try:
        folderName = str(userId)
    except:
        folderName = userId
    if folderName in ftp.nlst():
        ftp.cwd('/web/images/stories/Ostatne/sledovanie_upload/%s' %folderName)       
    else:
        ftp.mkd(str(folderName))
        ftp.cwd('/web/images/stories/Ostatne/sledovanie_upload/%s' %folderName)
    
    os.chdir(source)

    try:
        image = Image.open(filename)
        w, h = image.size
        if w or h > 1024:
            #resize

            if w > h:
                #landscape mode
                #resize on w = 1024 (out_image_size)
                #need to calculate h
                print("LOG: original w side is %s and h side is %s") %(w,h)
                longer_side = w
                resize_factor = longer_side / float(out_image_size)
                print("LOG: resize factore is %s") %resize_factor
                out_h_size = h / resize_factor
                print("LOG: h side after division is %s") %out_h_size
                out_h_size = int(out_h_size)
                print("LOG: h side after making it INT is %s") %out_h_size
                #resize
                print("LOG: resized w side is %s and h side is %s") %(out_image_size,out_h_size)
                image = image.resize((out_image_size, out_h_size), Image.ANTIALIAS)
                image.save(filename, 'JPEG', quality=out_image_quality)
            else:
                #portrait mode
                #resize h = 1024 (out_image_size)
                #need to calculate w
                longer_side = h
                resize_factor = longer_side / out_image_size
                out_w_size = w / resize_factor

                #resize
                image = image.resize((int(out_w_size), out_image_size), Image.ANTIALIAS)
                image.save(filename, 'JPEG', quality=out_image_quality)


    except:
        print("image resize failed")


    myfile = open(filename, 'r')
    ftp.storbinary("STOR " + filename, myfile)
    myfile.close()
    ftp.quit()


def delete_openshift_img(filename,userId):
    ftp = ftplib.FTP('cestasnp.sk')
    ftp.login("cestasnp.sk",'kockovo1256')
    ftp.cwd('/web/images/stories/Ostatne/sledovanie_upload') 
    ftp.cwd('/web/images/stories/Ostatne/sledovanie_upload/%s' %userId)
    
    ftp.delete('%s' %filename)
    ftp.quit()
