import gc
import machine
import time
import ssd1306

print(gc.mem_free())

import font

print(gc.mem_free())
gc.collect()
print(gc.mem_free())


def readglyph(c):
    i = font.remap_from.find(c)
    if i >= 0:
        c = font.remap_to[i]
    i = font.index.find(c)
    if i < 0:
        i = font.index.find('▯')
    addr0 = 0 if i == 0 else font.map_addr[i-1]
    addr1 = font.map_addr[i]
    return memoryview(font.bitmap)[addr0:addr1]


def text2vlsb(text):
    out = b''
    for c in text:
        glyph = readglyph(c)
        if out and glyph:
            left = out[-1]
            right = glyph[0]
            if left&right or (left>>1)&right or left&(right>>1):
                out += b'\x00' + glyph
            else:
                out += glyph
        else:
            out += glyph
    return out


# def print_vlsb(vlsb):
#     for y in range(8):
#         for c in vlsb:
#             if c & 1<<y:
#                 print('##', end='')
#             else:
#                 print('  ', end='')
#         print()
#
#print_vlsb(text2vlsb('Hello,'))
#print_vlsb(text2vlsb('world!'))


class TextDisplay:
    def __init__(self, disp):
        self.disp = disp
        self.lines = disp.height // 8
        self.line = 0
        self.linebuf = ''
        self.linebuf_vlsb = b''
        self.disp.fill(0)
    
    def buf_flush(self):
        if self.line >= 0 and self.line < self.lines:
            addr1 = self.disp.width * self.line
            addr2 = addr1+len(self.linebuf_vlsb)
            disp.buffer[addr1:addr2]=self.linebuf_vlsb
        self.linebuf = ''
        self.linebuf_vlsb = b''
        self.line += 1

    def print_word(self, word):
        word_nohyp = word.replace('\u00ad', '')
        word_vlsb = text2vlsb(word_nohyp)
        pxl_avail = self.disp.width - len(self.linebuf_vlsb)

        if len(word_vlsb) <= pxl_avail:
            self.linebuf += word_nohyp
            self.linebuf_vlsb += word_vlsb
            return

        if '\u00ad' in word:
            syllables = word.split('\u00ad')
            for i in range(len(syllables)-1, 0, -1):
                head = ''.join(syllables[:i]) + '-'
                tail = '\u00ad'.join(syllables[i:])
                head_vlsb = text2vlsb(head)
                if len(head_vlsb) <= pxl_avail:
                    self.linebuf += head
                    self.linebuf_vlsb += head_vlsb
                    self.buf_flush()
                    self.print_word(tail)
                    return

        if not word[0].isspace():
            if self.linebuf:
                self.buf_flush()
                self.print_word(word)
            else:
                if len(word_vlsb) > self.disp.width:
                    # TODO: handle VeryVeryLongMaybeGermanWords
                    print('Word', word_nohyp, 'is too long!')
                    word_vlsb = word_vlsb[:self.disp.width]
                self.linebuf, self.linebuf_vlsb = word_nohyp, word_vlsb

    def print_line(self, line):
        buf = ''
        for c in line:
            if c.isspace():
                if buf:
                    self.print_word(buf)
                    buf = ''
                self.print_word(c)
            else:
                buf += c
        if buf:
            self.print_word(buf)
        self.buf_flush()

    def show(self):
        if self.linebuf:
            self.buf_flush()
        self.disp.show()


def show_page(disp, start_file_line, start_screen_line):
    txt = TextDisplay(disp)
    txt.line = -start_screen_line
    file_lines = anchor = 0
    with open('book.txt') as f:
        for line in f:
            file_lines += 1
            if file_lines >= start_file_line:
                anchor = txt.line
                txt.print_line(line.rstrip())
            if txt.line >= txt.lines:
                break
    txt.show()
    if file_lines == start_file_line:
        return (start_file_line, start_screen_line+txt.lines)
    return (file_lines, txt.lines-anchor)


i2c = machine.SoftI2C(sda=machine.Pin(4), scl=machine.Pin(5))
disp = ssd1306.SSD1306_I2C(128, 32, i2c)
disp.contrast(0)
gc.collect()
rtc = machine.RTC()

try:
    fl, sl = rtc.memory().decode().split(' ')
    fl, sl = int(fl), int(sl)
except (ValueError, AttributeError):
    fl, sl = 0, 0

fl, sl = show_page(disp, fl, sl)
gc.collect()

rtc.memory(('%d %d' % (fl, sl)).encode())

time.sleep(5)
machine.deepsleep()
