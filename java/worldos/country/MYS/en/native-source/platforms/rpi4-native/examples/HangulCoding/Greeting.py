import English

def greet(name):
    greeting = "안녕하세요 " + name
    English.writeFile("Greeting.txt", greeting)
    English.Output(English.decodeText(English.readFile("Greeting.txt")))

greet("누리")
