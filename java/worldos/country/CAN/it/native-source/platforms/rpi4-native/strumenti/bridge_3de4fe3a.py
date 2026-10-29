"""Layer-2/SLIP bridge. TCP, UDP and FTP are processed by the guest, not Python.

QEMU's user network supplies NAT/host forwarding. raspi4b has no emulated GENET,
so a second UART carries IPv4 packets to the guest's lwIP stack.
"""
import select
import socket
import struct
import threading
import time
import ipaddress
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, qemu_network

indirizzo_reale = bytes.fromhex('525400123456')
gateway_hardware_e_mail = bytes.fromhex('52550a000202')
indirizzo_Internet_VALORE = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class bridge_3de4fe3a:
    def __init__(자신, trasferimento_di_file_numero_di_porta=2121, 전달규칙들=(), acquisire=False, guest_e_mail=None, ID_host='127.0.0.1'):
        if not 1024 <= trasferimento_di_file_numero_di_porta <= 65535 or 50000 <= trasferimento_di_file_numero_di_porta <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        자신.trasferimento_di_file_numero_di_porta = trasferimento_di_file_numero_di_porta
        자신.ip_config = read_config(Path(__file__).resolve().parents[1])
        guest_e_mail = guest_e_mail or 자신.ip_config['IP']
        qemu_network(자신.ip_config, guest_e_mail)
        e_mail=ipaddress.IPv4Address(guest_e_mail)
        자신.guest_e_mail=str(e_mail); 자신.Regolari_e_mail=e_mail.packed
        e_mail=ipaddress.IPv4Address(ID_host)
        if e_mail.is_multicast or str(e_mail)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        자신.ID_host=str(e_mail)
        자신.acquisire = acquisire; 자신.log_di_analisi = []
        자신.전달규칙들 = []
        사용중주소 = {('tcp', trasferimento_di_file_numero_di_porta)} | {('tcp', dati_funzione) for dati_funzione in range(50000,50008)}
        for riga_VALORE_c689d407 in 전달규칙들:
            percorso_componente = riga_VALORE_c689d407.split(':')
            if len(percorso_componente) != 3 or percorso_componente[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            rete_ABI, host, guest = percorso_componente[0], int(percorso_componente[1]), int(percorso_componente[2])
            if not 1024 <= host <= 65535 or not 1 <= guest <= 65535 or (rete_ABI, host) in 사용중주소:
                raise ValueError('invalid or duplicate forward: ' + riga_VALORE_c689d407)
            사용중주소.add((rete_ABI, host)); 자신.전달규칙들.append((rete_ABI, host, guest))
        자신.수신창구들 = []
        for _ in range(2):
            server_VALORE = socket.socket()
            server_VALORE.bind(('127.0.0.1', 0)); server_VALORE.listen(1); server_VALORE.setblocking(False)
            자신.수신창구들.append(server_VALORE)
        자신.접속자들 = [None, None]
        자신.reparto_IT_In_sospeso = [bytearray(), bytearray()]
        자신.Ethernet = bytearray(); 자신.seriale_datagramma = bytearray(); 자신.탈출됨 = 자신.reparto_IT_non_valida = False
        자신.Pause_evento = threading.Event(); 자신.errore = None
        자신.커널수신틀수 = 자신.커널발신틀수 = 0
        자신.esecutoreAsincrono = threading.Thread(target=자신.Cicli_VALORE, daemon=True)
        자신.esecutoreAsincrono.start()

    def 전달인수(자신):
        porta_COM_numero, porta_Ethernet = [stringa_dati.getsockname()[1] for stringa_dati in 자신.수신창구들]
        전달규칙 = 'user,id=wan,' + qemu_network(자신.ip_config, 자신.guest_e_mail) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(자신.trasferimento_di_file_numero_di_porta, 자신.guest_e_mail)
        for numero_di_porta in range(50000, 50008):
            전달규칙 += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(numero_di_porta, 자신.guest_e_mail)
        for rete_ABI, host, guest in 자신.전달규칙들:
            전달규칙 += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(rete_ABI, host, 자신.guest_e_mail, guest)
        전달규칙=전달규칙.replace('127.0.0.1:',자신.ID_host+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(porta_COM_numero),
                '-serial', 'chardev:slip', '-netdev', 전달규칙,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(porta_Ethernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def esecuzione_frame(자신, pacchetto_dati):
        자신.reparto_IT_In_sospeso[1] += struct.pack('!I', len(pacchetto_dati)) + pacchetto_dati

    def analisi_pacchetto(자신, direzione, pacchetto_dati):
        if not 자신.acquisire or len(pacchetto_dati)<20: return
        SCARTO_VALORE=(pacchetto_dati[0]&15)*4
        voce_VALORE={'time':time.monotonic(),'direction':direzione,'bytes':len(pacchetto_dati),'protocol':pacchetto_dati[9]}
        if pacchetto_dati[9]==6 and len(pacchetto_dati)>=SCARTO_VALORE+20:
            원본자료,meta_dati_e_mail,ordine_numero,확인번호,configurazione_BITS,Finestra=struct.unpack_from('!HHIIHH',pacchetto_dati,SCARTO_VALORE)
            voce_VALORE.update(source=원본자료,destination=meta_dati_e_mail,seq=ordine_numero,ack=확인번호,flags=configurazione_BITS&255,window=Finestra,
                        payload=len(pacchetto_dati)-SCARTO_VALORE-((pacchetto_dati[SCARTO_VALORE+12]>>4)*4))
        자신.log_di_analisi.append(voce_VALORE)
        if len(자신.log_di_analisi)>2048: del 자신.log_di_analisi[:1024]

    def SLIP_input(자신, dati):
        for punto_di_codice in dati:
            if punto_di_codice == 192:
                if 자신.seriale_datagramma and not 자신.reparto_IT_non_valida and not 자신.탈출됨:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(자신.seriale_datagramma)>=20 and 자신.seriale_datagramma[0]>>4==4:
                        e_mail=bytes(자신.seriale_datagramma[12:16])
                        try:
                            qemu_network(자신.ip_config, str(ipaddress.IPv4Address(e_mail)))
                            자신.Regolari_e_mail=e_mail
                        except ValueError:
                            pass
                    자신.analisi_pacchetto('from_guest',자신.seriale_datagramma)
                    자신.esecuzione_frame(gateway_hardware_e_mail + indirizzo_reale + b'\x08\x00' + 자신.seriale_datagramma)
                    자신.커널발신틀수 += 1
                자신.seriale_datagramma.clear(); 자신.탈출됨 = 자신.reparto_IT_non_valida = False
            elif punto_di_codice == 219 and not 자신.탈출됨:
                자신.탈출됨 = True
            else:
                if 자신.탈출됨:
                    if punto_di_codice not in (220, 221): 자신.reparto_IT_non_valida = True
                    punto_di_codice = 192 if punto_di_codice == 220 else 219
                    자신.탈출됨 = False
                if len(자신.seriale_datagramma) < 1600: 자신.seriale_datagramma.append(punto_di_codice)
                else: 자신.reparto_IT_non_valida = True

    def Ethernet_input(자신, dati):
        자신.Ethernet += dati
        while len(자신.Ethernet) >= 4:
            articolo_CONTA_NUMERI = struct.unpack_from('!I', 자신.Ethernet)[0]
            if articolo_CONTA_NUMERI > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(자신.Ethernet) < articolo_CONTA_NUMERI + 4: return
            esecuzione_frame = bytes(자신.Ethernet[4:4+articolo_CONTA_NUMERI]); del 자신.Ethernet[:4+articolo_CONTA_NUMERI]
            if len(esecuzione_frame) < 14: continue
            if esecuzione_frame[12:14] == b'\x08\x06' and len(esecuzione_frame) >= 42:
                risoluzione_dell_indirizzo_pacchetto = esecuzione_frame[14:42]
                if risoluzione_dell_indirizzo_pacchetto[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and risoluzione_dell_indirizzo_pacchetto[24:28] == 자신.Regolari_e_mail:
                    risposta = risoluzione_dell_indirizzo_pacchetto[:6] + b'\x00\x02' + indirizzo_reale + 자신.Regolari_e_mail + risoluzione_dell_indirizzo_pacchetto[8:18]
                    자신.esecuzione_frame(esecuzione_frame[6:12] + indirizzo_reale + b'\x08\x06' + risposta)
            elif esecuzione_frame[12:14] == b'\x08\x00':
                pacchetto_dati = esecuzione_frame[14:]
                자신.analisi_pacchetto('to_guest',pacchetto_dati)
                자신.reparto_IT_In_sospeso[0] += b'\xc0' + pacchetto_dati.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                자신.커널수신틀수 += 1

    def Cicli_VALORE(자신):
        try:
            while not 자신.Pause_evento.is_set():
                읽기대상들 = [stringa_dati for 순번, stringa_dati in enumerate(자신.수신창구들) if 자신.접속자들[순번] is None]
                읽기대상들 += [stringa_dati for stringa_dati in 자신.접속자들 if stringa_dati is not None]
                쓰기대상들 = [stringa_dati for 순번, stringa_dati in enumerate(자신.접속자들) if stringa_dati is not None and 자신.reparto_IT_In_sospeso[순번]]
                읽을수있음, scrivibile, _ = select.select(읽기대상들, 쓰기대상들, [], .05)
                for stringa_dati in 읽을수있음:
                    if stringa_dati in 자신.수신창구들:
                        순번 = 자신.수신창구들.index(stringa_dati); 자신.접속자들[순번], _ = stringa_dati.accept(); 자신.접속자들[순번].setblocking(False)
                    else:
                        순번 = 자신.접속자들.index(stringa_dati); dati = stringa_dati.recv(16384)
                        if not dati: return
                        (자신.SLIP_input if 순번 == 0 else 자신.Ethernet_input)(dati)
                for stringa_dati in scrivibile:
                    순번 = 자신.접속자들.index(stringa_dati)
                    try: articolo_CONTA_NUMERI = stringa_dati.send(자신.reparto_IT_In_sospeso[순번])
                    except BlockingIOError: continue
                    del 자신.reparto_IT_In_sospeso[순번][:articolo_CONTA_NUMERI]
                if any(len(SECONDO_VALORE) > 1024 * 1024 for SECONDO_VALORE in 자신.reparto_IT_In_sospeso):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as 보조항목:
            if not 자신.Pause_evento.is_set(): 자신.errore = str(보조항목)

    def Chiudi(자신):
        자신.Pause_evento.set(); 자신.esecutoreAsincrono.join(timeout=2)
        for stringa_dati in 자신.수신창구들 + 자신.접속자들:
            if stringa_dati is not None: stringa_dati.close()

    def __enter__(자신): return 자신
    def __exit__(자신, *argomento_array): 자신.Chiudi()
