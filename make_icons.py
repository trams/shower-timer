#!/usr/bin/env python3
"""Generate app icons. Run once: python3 make_icons.py"""
import os
import struct
import zlib

def make_png(size, bg=(0,0,0), fg=(0,224,64)):
    """Create a minimal PNG with a stopwatch glyph."""
    w = h = size
    pixels = []
    cx, cy = w / 2, h / 2
    outer_r = w * 0.38
    inner_r = w * 0.28
    hand_len = w * 0.22
    crown_w = w * 0.08
    crown_h = w * 0.06

    for y in range(h):
        row = []
        for x in range(w):
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            # outer ring
            on_ring = outer_r - w*0.04 <= dist <= outer_r
            # inner dial
            on_dial = dist <= inner_r
            # 12-o'clock hand (vertical up)
            on_hand = (abs(dx) <= w*0.025 and -hand_len <= dy <= 0 and dist <= inner_r)
            # crown (button on top)
            on_crown = (abs(dx) <= crown_w/2 and
                        -(outer_r + crown_h) <= dy <= -outer_r + w*0.02)
            if on_ring or on_dial or on_hand or on_crown:
                row.extend(fg)
            else:
                row.extend(bg)
        pixels.append(bytes(row))

    def chunk(tag, data):
        c = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', c)

    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    raw = b''.join(b'\x00' + row for row in pixels)
    idat = zlib.compress(raw, 9)

    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', idat)
            + chunk(b'IEND', b''))

os.makedirs('icons', exist_ok=True)

for name, size, fg in [
    ('icon-192.png',         192, (0, 224, 64)),
    ('icon-512.png',         512, (0, 224, 64)),
    ('icon-maskable-512.png',512, (0, 200, 56)),
]:
    path = os.path.join('icons', name)
    with open(path, 'wb') as f:
        f.write(make_png(size, fg=fg))
    print(f'Written {path}')

print('Icons generated.')
