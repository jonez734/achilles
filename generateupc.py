from io import BytesIO

from barcode import UPCA
from barcode.writer import ImageWriter

# print to a file-like object:
rv = BytesIO()
UPCA(str(100000902922), writer=ImageWriter()).write(rv)

# or sure, to an actual file:
with open("somefile.png", "wb") as f:
    UPCA("100000011111", writer=ImageWriter()).write(f)
