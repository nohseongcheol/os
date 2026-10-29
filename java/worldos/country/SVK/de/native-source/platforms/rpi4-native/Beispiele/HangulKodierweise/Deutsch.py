"""eigen betriebskernWert MicroPython에서 사용하는 한글 Funktion Name."""
import jkoros as Betriebssystem
Ausgabe = print
dateiLesen = Betriebssystem.read
dateiSchreiben = Betriebssystem.write
dateiEntfernen = Betriebssystem.remove
eingabeLesen = Betriebssystem.stdin
rechteckZeichnen = Betriebssystem.rect
fürZeichnungWarten = Betriebssystem.wait_key
millisekunden = Betriebssystem.ticks_ms
datagrammÖffnen = Betriebssystem.udp_open
datagrammSenden = Betriebssystem.udp_send
externDatagrammSenden = Betriebssystem.udp_sendto
datagrammEmpfangen = Betriebssystem.udp_recv
netzwerkSchließen = Betriebssystem.udp_close

def textDekodieren(Daten):
    return Daten.decode("utf-8")
