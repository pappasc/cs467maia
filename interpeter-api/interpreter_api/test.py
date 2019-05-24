image = open('kvavlen_sig.jpg', 'r')
image_on_disk = image.read()
image2 = open('kvavlen_sig2.jpg', 'w')
image_on_disk2 = image2.write(image_on_disk)