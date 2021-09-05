
You are given a small part of one large image of a field. The image has one problem, it consists of two parts: the left part is dark, while the right part is brighter. Check full.jpg to see how it looks in RGB. The dividing line between the two parts is not very straight. The task is to somehow find and remove the dividing line. For example, you can make the dark part brighter so that the line becomes almost invisible to human eye. For simplicity, you are given only one channel of the image (red) and only the top middle part of the full image. The pixels are encoded as 16-bit unsigned integers (uint16), so regular image preview applications on your computer may not be able to open it. But OpenCV can! 

Your python script should have the following signature:
python remove_line.py --input red.tif --output red_no_line.tif

We recommend to use argparse, numpy and cv2 in your program.