"""The characters a captured terminal frame may use: exactly what the Writfold Term subset font holds."""
# ASCII; middle dot, multiplication sign, dashes, ellipsis; arrows; box drawing; geometric shapes; check and cross.
RANGES = [(0x20, 0x7E), (0xB7, 0xB7), (0xD7, 0xD7), (0x2013, 0x2014), (0x2026, 0x2026), (0x2190, 0x2193),
          (0x2500, 0x257F), (0x25A0, 0x25CF), (0x2713, 0x2713), (0x2717, 0x2717)]

def uncovered(text):
    """The characters of `text`, newlines aside, that the subset font does not hold."""
    return sorted({ch for ch in text if ch != "\n" and not any(lo <= ord(ch) <= hi for lo, hi in RANGES)})
