from math import sin

constantesMD5 = [int(abs(sin(i + 1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]

def md5(message):
    cpmessage=message
    cpmessage=bytearray(message.encode())
    originalsize = (len(cpmessage) * 8) & 0xffffffffffffffff
    size64 = originalsize.to_bytes(8, byteorder='little')

    r = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
         5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
         4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
         6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

    # PADDING
    cpmessage.append(0x80)
    while (len(cpmessage)) % 64 != 56:
        cpmessage.append(0)
    cpmessage += size64

    # preparation des variable
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476

    for offset in range(0, len(cpmessage), 64):
        block = cpmessage[offset: offset+64]
        a = h0
        b = h1
        c = h2
        d = h3

        for i in range(64):
            if i < 16:
                f = ((c & b) | ((~b) & d))
                g = i
            elif i < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * i) % 16
        #Update des variable
            temp = d
            d = c
            c = b
            #rotation
            x = (a + f + constantesMD5[i] + int.from_bytes(block[g * 4: 4 * g + 4], byteorder='little'))& 0xFFFFFFFF
            rotated = (x << r[i] | x >> (32 - r[i])) & 0xFFFFFFFF

            b = (rotated+ b)&0xFFFFFFFF
            a = temp

        #incrémentation et masquage
        h0 = (a + h0)&0xFFFFFFFF
        h1 = (b + h1)&0xFFFFFFFF
        h2 = (c + h2)&0xFFFFFFFF
        h3 = (d + h3)&0xFFFFFFFF

    #Hash brute en little endian
    hashraw = (h0 | (h1 << 32) | (h2 << 64) | h3 << 96) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    #print("hashraw", hex(hashraw))
    result = '{:032x}'.format(int.from_bytes(hashraw.to_bytes(16, byteorder="little"), 'big'))

    return (result)
