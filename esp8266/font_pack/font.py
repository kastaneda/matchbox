remap_from = 'ʼ’АВЕІКМНОРСТХаеіорсух¦µ⌀'
remap_to = "''ABEIKMHOPCTXaeiopcyx|μ∅"
index = 'ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz O0123456789!"#$%&\'()*+,-./:;<=>?@`[\\]^_{|}~БГҐДЄЁЖЗИЇЙЛПУЎФЦЧШЩЪЫЬЭЮЯбвгґдєёжзиїйклмнптўфцчшщъыьэюяÄäÖöÜüẞßŁłźżĄąĘęćśóńčřžňšμΩΣπαβσΔδεωρτφψ«»°–—©§·•№⌘¶₴€£¥¤×÷±≈∅▯'
with open("font_map_addr.bin", "rb") as f:
    map_addr = bytearray(f.read())
with open("font_bitmap.bin", "rb") as f:
    bitmap = bytearray(f.read())
