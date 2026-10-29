import jkoros
print("MicroPython on Java kernel · 안녕하세요 · 😀")
print("squares:", [수 * 수 for 수 in range(6)])
jkoros.write("python.txt", "한글 קובץ\n")
print(jkoros.read("python.txt").decode())
jkoros.rect(470, 300, 48, 32, 0x40c050)
