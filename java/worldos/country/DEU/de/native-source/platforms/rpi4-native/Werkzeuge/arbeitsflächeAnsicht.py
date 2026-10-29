#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, tasteWert 입력은 eigen betriebskernWert UART로 전달한다. localhost 전용, 단일 steuerungWert 클라이언트.
RFB 3.8: https://www.rfc-editor.org/rfc/rfc6143.html
"""
import argparse
from contextlib import ExitStack
from pathlib import Path
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from befehlAusführen import befehl
from local_input import create


def exaktWert(netzbuchseWert, größe):
    Daten = bytearray()
    while len(Daten) < größe:
        fragmentWert = netzbuchseWert.recv(größe - len(Daten))
        if not fragmentWert: raise EOFError()
        Daten.extend(fragmentWert)
    return bytes(Daten)


class Tastatur:
    def __init__(selbstWert, senden, betriebsartGeändert=None):
        selbstWert.übertragungBytes = senden; selbstWert.modifikatorTaste = set(); selbstWert.zwischenablageWert = b''
        selbstWert.HangulZusammensetzer = create(senden, Path(__file__).resolve().parents[1]); selbstWert.koreanisch = False; selbstWert.umschaltenTaste = set()
        selbstWert.unicodeEingabe = None
        selbstWert.betriebsartGeändert = betriebsartGeändert
        if betriebsartGeändert: betriebsartGeändert(False)

    def senden(selbstWert, Daten):
        selbstWert.HangulZusammensetzer.bestätigenZusammensetzung()
        selbstWert.übertragungBytes(Daten)

    def umschaltenBetriebsart(selbstWert):
        selbstWert.HangulZusammensetzer.bestätigenZusammensetzung(); selbstWert.koreanisch = not selbstWert.koreanisch
        if selbstWert.betriebsartGeändert: selbstWert.betriebsartGeändert(selbstWert.koreanisch)

    def gedrücktWert(selbstWert, istDrückend, tasteSymbol):
        if tasteSymbol in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if istDrückend: selbstWert.modifikatorTaste.add(tasteSymbol)
            else: selbstWert.modifikatorTaste.discard(tasteSymbol)
            return
        if not istDrückend:
            selbstWert.umschaltenTaste.discard(tasteSymbol)
            return
        steuerungTaste = bool(selbstWert.modifikatorTaste & {0xffe3, 0xffe4})
        verschiebenTaste = bool(selbstWert.modifikatorTaste & {0xffe1, 0xffe2})
        if steuerungTaste and verschiebenTaste and tasteSymbol in (ord('u'),ord('U')):
            selbstWert.HangulZusammensetzer.bestätigenZusammensetzung(); selbstWert.unicodeEingabe = ''; return
        if selbstWert.unicodeEingabe is not None:
            if tasteSymbol in (32,0xff0d):
                try:
                    Wert=int(selbstWert.unicodeEingabe,16)
                    if 32<=Wert<=0x10ffff and not 0xd800<=Wert<=0xdfff: selbstWert.senden(chr(Wert).encode('utf-8'))
                except ValueError: pass
                selbstWert.unicodeEingabe=None
            elif tasteSymbol==0xff1b: selbstWert.unicodeEingabe=None
            elif tasteSymbol==0xff08: selbstWert.unicodeEingabe=selbstWert.unicodeEingabe[:-1]
            elif tasteSymbol<128 and chr(tasteSymbol) in '0123456789abcdefABCDEF' and len(selbstWert.unicodeEingabe)<6: selbstWert.unicodeEingabe+=chr(tasteSymbol)
            return
        if tasteSymbol in (0xff31,0xffc6) or tasteSymbol==32 and verschiebenTaste and not steuerungTaste:
            if tasteSymbol not in selbstWert.umschaltenTaste: selbstWert.umschaltenBetriebsart()
            selbstWert.umschaltenTaste.add(tasteSymbol)
            return
        if tasteSymbol==0xff08 and selbstWert.koreanisch and not steuerungTaste and selbstWert.HangulZusammensetzer.rückschritt(): return
        if steuerungTaste and verschiebenTaste and tasteSymbol in (ord('t'),ord('T')):
            selbstWert.senden(bytes([30,2,1,0,0,0,0])); return
        if tasteSymbol==0xffc3: selbstWert.senden(bytes([30,2,2,0,0,0,0])); return
        if tasteSymbol==0xffc9: selbstWert.senden(bytes([30,2,3,0,0,0,0])); return
        if steuerungTaste and verschiebenTaste and tasteSymbol in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            selbstWert.senden(selbstWert.zwischenablageWert); return
        besondersTaste = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if tasteSymbol in besondersTaste: selbstWert.senden(besondersTaste[tasteSymbol]); return
        zeichenKodierung = tasteSymbol & 0xffffff if tasteSymbol & 0xff000000 == 0x01000000 else tasteSymbol
        if zeichenKodierung > 0x10ffff or 0xd800 <= zeichenKodierung <= 0xdfff or tasteSymbol >= 0xff00 and tasteSymbol < 0x1000000: return
        if steuerungTaste and 0x40 <= zeichenKodierung <= 0x7f: selbstWert.senden(bytes([zeichenKodierung & 31])); return
        if zeichenKodierung < 32: return
        if selbstWert.koreanisch and selbstWert.modifikatorTaste & {0xffea,0xfe03,0xff7e} and not steuerungTaste and hasattr(selbstWert.HangulZusammensetzer, 'profile'):
            if selbstWert.HangulZusammensetzer.zuführenTaste(chr(zeichenKodierung), altgr=True): return
        voranstehendTeil = b'\x1b' if selbstWert.modifikatorTaste & {0xffe9, 0xffea} else b''
        if selbstWert.koreanisch and not steuerungTaste and not voranstehendTeil and 32<=zeichenKodierung<127:
            zeichenDaten=chr(zeichenKodierung).upper() if verschiebenTaste else chr(zeichenKodierung)
            if selbstWert.HangulZusammensetzer.zuführenTaste(zeichenDaten): return
        selbstWert.senden(voranstehendTeil + chr(zeichenKodierung).encode('utf-8'))


class arbeitsflächeVerbinden:
    def __init__(selbstWert, prozess):
        selbstWert.prozess=prozess; selbstWert.sperreWert=threading.Lock(); selbstWert.vorbereitungFertig=False; selbstWert.terminal=False; selbstWert.anfänglichBildschirm=False; selbstWert.istGeschlossen=False

    def senden(selbstWert, Daten):
        if not Daten or selbstWert.istGeschlossen: return
        with selbstWert.sperreWert:
            try: selbstWert.prozess.stdin.write(Daten); selbstWert.prozess.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def seriellEinAusgabe(selbstWert):
        endungTeil=b''
        try:
            while True:
                Daten=selbstWert.prozess.stdout.read(4096)
                if not Daten: break
                sys.stdout.buffer.write(Daten); sys.stdout.buffer.flush()
                endungTeil=(endungTeil+Daten)[-8192:]
                geöffnet=endungTeil.rfind(b'TERMINAL READY'); istGeschlossen=endungTeil.rfind(b'TERMINAL CLOSED'); zeichnungBildschirm=endungTeil.rfind(b'GUI READY:'); hatVerlassen=endungTeil.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(geöffnet,istGeschlossen,zeichnungBildschirm,hatVerlassen)>=0:
                    selbstWert.terminal=geöffnet>max(istGeschlossen,zeichnungBildschirm,hatVerlassen)
                    selbstWert.anfänglichBildschirm=zeichnungBildschirm>max(geöffnet,istGeschlossen,hatVerlassen)
                if not selbstWert.vorbereitungFertig and b'jkoros-native> ' in endungTeil:
                    selbstWert.vorbereitungFertig=True; selbstWert.senden(b'terminal\n')
        finally: selbstWert.istGeschlossen=True

    def anfragestelle(selbstWert, anfragestelle, pfad):
        dienstanbieterWert=socket.socket(socket.AF_UNIX); dienstanbieterWert.settimeout(10); anfragestelle.settimeout(10)
        tastaturEintrag=Tastatur(selbstWert.senden,lambda koreanisch:selbstWert.senden(bytes([30,3,int(koreanisch),0,0,0,0])))
        vorherigSchaltflächen=0
        try:
            dienstanbieterWert.connect(str(pfad))
            # anfänglichStatuswert 협상은 순서대로 끝낸다. danachWert Ausgabe 가닥만 클라이언트에 쓴다.
            anfragestelle.sendall(exaktWert(dienstanbieterWert,12))
            versionNummer=exaktWert(anfragestelle,12)
            if versionNummer not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            dienstanbieterWert.sendall(versionNummer)
            elementeintragAnzahl=exaktWert(dienstanbieterWert,1);anfragestelle.sendall(elementeintragAnzahl+exaktWert(dienstanbieterWert,elementeintragAnzahl[0]))
            sicherheit=exaktWert(anfragestelle,1)
            if sicherheit!=b'\x01': raise ValueError('unexpected security type')
            dienstanbieterWert.sendall(sicherheit)
            if versionNummer==b'RFB 003.008\n':anfragestelle.sendall(exaktWert(dienstanbieterWert,4))
            dienstanbieterWert.sendall(exaktWert(anfragestelle,1))
            anfänglichWert=exaktWert(dienstanbieterWert,24)
            anfragestelle.sendall(anfänglichWert+exaktWert(dienstanbieterWert,struct.unpack('>I',anfänglichWert[20:])[0]))
            bildpunktBytes=anfänglichWert[4]//8;zeigerUnterstützt=False
            anfragestelle.settimeout(None);dienstanbieterWert.settimeout(None)
            def ausgabe():
                try:
                    while True:
                        kategorieWert=exaktWert(dienstanbieterWert,1)[0]
                        if kategorieWert==0:
                            kopfWert=exaktWert(dienstanbieterWert,3);eintragAnzahl=struct.unpack('>H',kopfWert[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 entferntWert 포인터의 중복을 피한다.
                            verborgenWert=zeigerUnterstützt
                            if verborgenWert:anfragestelle.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            anfragestelle.sendall(bytes([kategorieWert])+kopfWert)
                            for _ in range(eintragAnzahl):
                                rechteck=exaktWert(dienstanbieterWert,12);waagerechtPosition,senkrechtPosition,breiteSpannweite,höheWert,kodierungWert=struct.unpack('>HHHHi',rechteck)
                                if kodierungWert!=0:raise ValueError('unexpected framebuffer encoding: '+str(kodierungWert))
                                anfragestelle.sendall(rechteck)
                                restwertDaten=breiteSpannweite*höheWert*bildpunktBytes
                                while restwertDaten:
                                    Daten=exaktWert(dienstanbieterWert,min(restwertDaten,65536));anfragestelle.sendall(Daten);restwertDaten-=len(Daten)
                        elif kategorieWert==1:
                            kopfWert=exaktWert(dienstanbieterWert,5);elementeintragAnzahl=struct.unpack('>H',kopfWert[3:])[0]
                            anfragestelle.sendall(bytes([kategorieWert])+kopfWert+exaktWert(dienstanbieterWert,elementeintragAnzahl*6))
                        elif kategorieWert==2:anfragestelle.sendall(bytes([kategorieWert]))
                        elif kategorieWert==3:
                            kopfWert=exaktWert(dienstanbieterWert,7);elementeintragAnzahl=struct.unpack('>I',kopfWert[3:])[0]
                            if elementeintragAnzahl>1048576:raise ValueError('server clipboard too large')
                            anfragestelle.sendall(bytes([kategorieWert])+kopfWert+exaktWert(dienstanbieterWert,elementeintragAnzahl))
                        else:raise ValueError('unexpected RFB server message: '+str(kategorieWert))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:anfragestelle.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            hintergrundarbeiter=threading.Thread(target=ausgabe,daemon=True);hintergrundarbeiter.start()
            while not selbstWert.istGeschlossen:
                kategorieWert=exaktWert(anfragestelle,1)[0]
                if kategorieWert==4:
                    rumpfText=exaktWert(anfragestelle,7); tastaturEintrag.gedrücktWert(rumpfText[0]!=0,struct.unpack('>I',rumpfText[3:])[0]); continue
                if kategorieWert==255:
                    rumpfText=exaktWert(anfragestelle,11)
                    if rumpfText[0]!=0: raise ValueError('unsupported QEMU input extension')
                    tastaturEintrag.gedrücktWert(struct.unpack('>H',rumpfText[1:3])[0]!=0,struct.unpack('>I',rumpfText[3:7])[0]); continue
                if kategorieWert==5:
                    rumpfText=exaktWert(anfragestelle,5); schaltflächen,waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate=struct.unpack('>BHH',rumpfText)
                    istGedrückt=schaltflächen&~vorherigSchaltflächen; vorherigSchaltflächen=schaltflächen
                    if istGedrückt: tastaturEintrag.HangulZusammensetzer.bestätigenZusammensetzung()
                    if istGedrückt&1 and selbstWert.anfänglichBildschirm and 64<=waagerechteKoordinateKoordinate<576 and 112<=senkrechteKoordinateKoordinate<372:
                        nachschlagenIndex=(senkrechteKoordinateKoordinate-112)//52
                        if (senkrechteKoordinateKoordinate-112)%52<40 and nachschlagenIndex<5: selbstWert.senden(bytes([ord('1')+nachschlagenIndex]))
                    else: selbstWert.senden(bytes([30,1,schaltflächen,waagerechteKoordinateKoordinate&255,waagerechteKoordinateKoordinate>>8,senkrechteKoordinateKoordinate&255,senkrechteKoordinateKoordinate>>8]))
                    continue
                if kategorieWert==6:
                    rumpfText=exaktWert(anfragestelle,7); Länge=struct.unpack('>i',rumpfText[3:])[0]
                    if abs(Länge)>65536: raise ValueError('clipboard too large')
                    Text=exaktWert(anfragestelle,abs(Länge))
                    if Länge>=0:
                        try: tastaturEintrag.zwischenablageWert=Text.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: tastaturEintrag.zwischenablageWert=Text.decode('latin-1').encode('utf-8')
                        tastaturEintrag.zwischenablageWert=tastaturEintrag.zwischenablageWert[:65536].decode('utf-8','ignore').encode('utf-8')
                    dienstanbieterWert.sendall(bytes([kategorieWert])+rumpfText+Text); continue
                if kategorieWert==0:
                    rumpfText=exaktWert(anfragestelle,19)
                    if rumpfText[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    bildpunktBytes=rumpfText[3]//8
                elif kategorieWert==2:
                    rumpfText=exaktWert(anfragestelle,3); eintragAnzahl=struct.unpack('>H',rumpfText[1:])[0]
                    if eintragAnzahl>512: raise ValueError('too many encodings')
                    kodiertWerte=struct.unpack('>'+str(eintragAnzahl)+'i',exaktWert(anfragestelle,eintragAnzahl*4))
                    zeigerUnterstützt=-239 in kodiertWerte
                    # 로컬 Bildschirm 중계는 standardwertWert Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    rumpfText=struct.pack('>BHi',0,1,0)
                elif kategorieWert in (3,150): rumpfText=exaktWert(anfragestelle,9)
                elif kategorieWert==248:
                    rumpfText=exaktWert(anfragestelle,8)
                    if rumpfText[7]>64: raise ValueError('fence too large')
                    rumpfText+=exaktWert(anfragestelle,rumpfText[7])
                elif kategorieWert==250: rumpfText=exaktWert(anfragestelle,3)
                elif kategorieWert==251:
                    rumpfText=exaktWert(anfragestelle,7)
                    if rumpfText[5]>16: raise ValueError('too many screens')
                    rumpfText+=exaktWert(anfragestelle,rumpfText[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(kategorieWert))
                dienstanbieterWert.sendall(bytes([kategorieWert])+rumpfText)
        except (OSError,EOFError,ValueError) as fehler:
            if str(fehler): print('VNC client:',fehler,file=sys.stderr,flush=True)
        finally:
            for netzbuchseWert in (anfragestelle,dienstanbieterWert):
                try: netzbuchseWert.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                netzbuchseWert.close()


def arbeitsflächeAusführenVorgang(portNummer=5902, netzwerk=False, dateiÜbertragungPortNummer=2121, weiterleitendRegeln=(), auflösungWert=(640, 480), gastAdresse=None, wirtssystemAdresse='127.0.0.1'):
    with ExitStack() as betriebsmittel, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as arbeitendPfad:
        netzwerkBrückeEintrag = None
        if netzwerk:
            from netzwerkBrücke import netzwerkBrücke
            netzwerkBrückeEintrag = betriebsmittel.enter_context(netzwerkBrücke(dateiÜbertragungPortNummer, weiterleitendRegeln, gastAdresse=gastAdresse, wirtssystemAdresse=wirtssystemAdresse))
        pfad=Path(arbeitendPfad)/'display.sock'
        with socket.socket() as portEmpfangen:
            portEmpfangen.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            portEmpfangen.bind(('127.0.0.1',portNummer)); portEmpfangen.listen(1); portEmpfangen.settimeout(.2)
            vNCPort=portEmpfangen.getsockname()[1]
            if netzwerkBrückeEintrag and (vNCPort==dateiÜbertragungPortNummer or 50000<=vNCPort<=50007 or any(NetzwerkABI=='tcp' and Wirtssystem==vNCPort for NetzwerkABI,Wirtssystem,_ in netzwerkBrückeEintrag.weiterleitendRegeln)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            prozess=subprocess.Popen(befehl(auflösungWert)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(pfad)]+(netzwerkBrückeEintrag.weitergeleitetArgument() if netzwerkBrückeEintrag else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            brücke=arbeitsflächeVerbinden(prozess); leser=threading.Thread(target=brücke.seriellEinAusgabe,daemon=True); leser.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(portEmpfangen.getsockname()[1]),flush=True)
            if netzwerkBrückeEintrag: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(wirtssystemAdresse,dateiÜbertragungPortNummer),flush=True)
            def beendenProzess(signalNummer,ausführungRahmen): raise KeyboardInterrupt()
            vorherig=signal.signal(signal.SIGTERM,beendenProzess)
            verarbeitungAufgabe=None; unterbrochen=False
            try:
                while prozess.poll() is None:
                    try: anfragestelle,_=portEmpfangen.accept()
                    except socket.timeout: continue
                    if verarbeitungAufgabe is not None and verarbeitungAufgabe.is_alive(): anfragestelle.close(); continue
                    if not pfad.exists(): anfragestelle.close(); continue
                    verarbeitungAufgabe=threading.Thread(target=brücke.anfragestelle,args=(anfragestelle,pfad),daemon=True); verarbeitungAufgabe.start()
            except KeyboardInterrupt: unterbrochen=True
            finally:
                brücke.istGeschlossen=True
                if netzwerkBrückeEintrag: netzwerkBrückeEintrag.pausierenEreignis.set()
                if prozess.poll() is None:
                    prozess.terminate()
                    try: prozess.wait(timeout=5)
                    except subprocess.TimeoutExpired: prozess.kill(); prozess.wait()
                leser.join(timeout=2); prozess.stdin.close(); prozess.stdout.close(); signal.signal(signal.SIGTERM,vorherig)
            if netzwerkBrückeEintrag and netzwerkBrückeEintrag.fehler: raise RuntimeError('network bridge: '+netzwerkBrückeEintrag.fehler)
            return 0 if unterbrochen else prozess.returncode


if __name__=='__main__':
    from befehlAusführen import auflösungLesen
    strukturanalysierer=argparse.ArgumentParser(description=__doc__); strukturanalysierer.add_argument('--port',type=int,default=5902)
    strukturanalysierer.add_argument('--resolution',type=auflösungLesen,default=(640,480))
    strukturanalysierer.add_argument('--network',action='store_true'); strukturanalysierer.add_argument('--ftp-port',type=int,default=2121)
    strukturanalysierer.add_argument('--forward',action='append',default=[])
    argumentDatenfeld=strukturanalysierer.parse_args()
    if argumentDatenfeld.forward and not argumentDatenfeld.network: strukturanalysierer.error('--forward requires --network')
    raise SystemExit(arbeitsflächeAusführenVorgang(argumentDatenfeld.port,netzwerk=argumentDatenfeld.network,dateiÜbertragungPortNummer=argumentDatenfeld.ftp_port,weiterleitendRegeln=argumentDatenfeld.forward,auflösungWert=argumentDatenfeld.resolution))
