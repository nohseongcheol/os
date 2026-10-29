from English import Output, writeFile, readFile, encodeText, decodeText
data = "PYTHON file: English 😀\n"
writeFile("python.txt", encodeText(data))
readTextValue = decodeText(readFile("python.txt"))
assert readTextValue == data
Output(readTextValue, ending="")
