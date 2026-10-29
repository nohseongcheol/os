import jkoros
print("MicroPython on Java kernel · 안녕하세요 · 😀")
print("squares:", [número * número for número in range(6)])
jkoros.write("python.txt", "한글 ficheiro\n")
print(jkoros.read("python.txt").decode())
jkoros.rect(470, 300, 48, 32, 0x40c050)
