import qrcode
from PIL import Image

# Data to encode
data = "www.linkedin.com/in/saiprakash-kulkarni-7a167732a"  # You can change this to any text or URL

# Create QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data(data)
qr.make(fit=True)

# Create and show image
img = qr.make_image(fill_color="black", back_color="white")
img.show()  # This opens the QR code in your default image viewer
print("-------Fallow My LinkedIn Profile-------")