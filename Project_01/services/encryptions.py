from PIL import Image


def bytes_to_bits(data: bytes) -> str:
    return "".join(format(byte, "08b") for byte in data)


def bits_to_bytes(bits: str) -> bytes:
    return bytes(int(bits[i : i + 8], 2) for i in range(0, len(bits), 8))


def embed_data(image: Image.Image, payload: bytes) -> Image.Image:
    image = image.convert("RGB")

    bits = bytes_to_bits(payload)
    pixels = image.load()

    width, height = image.size

    capacity = width * height * 3

    if len(bits) > capacity:
        raise ValueError("Image too small for payload")

    bit_index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]  # type: ignore

            channels = [r, g, b]

            for i in range(3):
                if bit_index < len(bits):
                    channels[i] = (channels[i] & ~1) | int(bits[bit_index])
                    bit_index += 1

            pixels[x, y] = tuple(channels)  # type: ignore

            if bit_index >= len(bits):
                return image

    return image


def extract_data(image: Image.Image) -> bytes:
    image = image.convert("RGB")

    pixels = image.load()
    width, height = image.size

    bits = []

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]  # type: ignore

            bits.append(str(r & 1))
            bits.append(str(g & 1))
            bits.append(str(b & 1))

    data = bits_to_bytes("".join(bits))

    return data
