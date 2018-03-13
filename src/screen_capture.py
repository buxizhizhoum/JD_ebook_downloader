from PIL import ImageGrab

image = ImageGrab.grab()
image.save("../image/test.jpeg", "jpeg")
