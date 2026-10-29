import jkoros
print("MicroPython on Java kernel · 안녕하세요 · 😀")
print("squares:", [identyfikator * identyfikator for identyfikator in range(6)])
jkoros.write("python.txt", "한글 nazwa_pliku\n")
print(jkoros.read("python.txt").decode())
jkoros.rect(470, 300, 48, 32, 0x40c050)
