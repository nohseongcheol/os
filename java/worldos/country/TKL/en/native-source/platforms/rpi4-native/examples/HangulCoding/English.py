"""Native kernelValue MicroPython에서 사용하는 한글 functionValue name."""
import jkoros as OperatingSystem
Output = print
readFile = OperatingSystem.read
writeFile = OperatingSystem.write
removeFile = OperatingSystem.remove
readInput = OperatingSystem.stdin
drawRectangle = OperatingSystem.rect
waitForDrawing = OperatingSystem.wait_key
milliseconds = OperatingSystem.ticks_ms
openDatagram = OperatingSystem.udp_open
sendDatagram = OperatingSystem.udp_send
sendExternalDatagram = OperatingSystem.udp_sendto
receiveDatagram = OperatingSystem.udp_recv
closeNetwork = OperatingSystem.udp_close

def decodeText(data):
    return data.decode("utf-8")
