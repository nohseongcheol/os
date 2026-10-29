import jkoros
print("MicroPython on Java kernel · 안녕하세요 · 😀")
print("squares:", [ကိန်းတန်ဖိုး * ကိန်းတန်ဖိုး for ကိန်းတန်ဖိုး in range(6)])
jkoros.write("python.txt", "한글 ဖိုင်\n")
print(jkoros.read("python.txt").decode())
jkoros.rect(470, 300, 48, 32, 0x40c050)
