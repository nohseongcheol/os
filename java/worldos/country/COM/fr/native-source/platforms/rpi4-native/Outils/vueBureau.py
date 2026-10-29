#!/usr/bin/env python3
"""RFB 화면은 QEMU에서, valeurTouche 입력은 interne valeurNoyau UART로 전달한다. localhost 전용, 단일 valeurContrôle 클라이언트.
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
from exécuterCommande import commande
from local_input import create


def valeurExact(valeurPriseRéseau, taille):
    Données = bytearray()
    while len(Données) < taille:
        valeurFragment = valeurPriseRéseau.recv(taille - len(Données))
        if not valeurFragment: raise EOFError()
        Données.extend(valeurFragment)
    return bytes(Données)


class Clavier:
    def __init__(valeurSoi, envoyer, changéMode=None):
        valeurSoi.octetsTransfert = envoyer; valeurSoi.toucheModificateur = set(); valeurSoi.valeurPressePapiers = b''
        valeurSoi.ComposeurHangul = create(envoyer, Path(__file__).resolve().parents[1]); valeurSoi.coréen = False; valeurSoi.toucheCommuter = set()
        valeurSoi.entréeUnicode = None
        valeurSoi.changéMode = changéMode
        if changéMode: changéMode(False)

    def envoyer(valeurSoi, Données):
        valeurSoi.ComposeurHangul.compositionConfirmer()
        valeurSoi.octetsTransfert(Données)

    def modeCommuter(valeurSoi):
        valeurSoi.ComposeurHangul.compositionConfirmer(); valeurSoi.coréen = not valeurSoi.coréen
        if valeurSoi.changéMode: valeurSoi.changéMode(valeurSoi.coréen)

    def valeurEnfoncé(valeurSoi, estEnfoncementEnCours, symboleTouche):
        if symboleTouche in (0xffe1, 0xffe2, 0xffe3, 0xffe4, 0xffe9, 0xffea, 0xfe03, 0xff7e):
            if estEnfoncementEnCours: valeurSoi.toucheModificateur.add(symboleTouche)
            else: valeurSoi.toucheModificateur.discard(symboleTouche)
            return
        if not estEnfoncementEnCours:
            valeurSoi.toucheCommuter.discard(symboleTouche)
            return
        toucheContrôle = bool(valeurSoi.toucheModificateur & {0xffe3, 0xffe4})
        toucheDécaler = bool(valeurSoi.toucheModificateur & {0xffe1, 0xffe2})
        if toucheContrôle and toucheDécaler and symboleTouche in (ord('u'),ord('U')):
            valeurSoi.ComposeurHangul.compositionConfirmer(); valeurSoi.entréeUnicode = ''; return
        if valeurSoi.entréeUnicode is not None:
            if symboleTouche in (32,0xff0d):
                try:
                    valeur=int(valeurSoi.entréeUnicode,16)
                    if 32<=valeur<=0x10ffff and not 0xd800<=valeur<=0xdfff: valeurSoi.envoyer(chr(valeur).encode('utf-8'))
                except ValueError: pass
                valeurSoi.entréeUnicode=None
            elif symboleTouche==0xff1b: valeurSoi.entréeUnicode=None
            elif symboleTouche==0xff08: valeurSoi.entréeUnicode=valeurSoi.entréeUnicode[:-1]
            elif symboleTouche<128 and chr(symboleTouche) in '0123456789abcdefABCDEF' and len(valeurSoi.entréeUnicode)<6: valeurSoi.entréeUnicode+=chr(symboleTouche)
            return
        if symboleTouche in (0xff31,0xffc6) or symboleTouche==32 and toucheDécaler and not toucheContrôle:
            if symboleTouche not in valeurSoi.toucheCommuter: valeurSoi.modeCommuter()
            valeurSoi.toucheCommuter.add(symboleTouche)
            return
        if symboleTouche==0xff08 and valeurSoi.coréen and not toucheContrôle and valeurSoi.ComposeurHangul.retourArrière(): return
        if toucheContrôle and toucheDécaler and symboleTouche in (ord('t'),ord('T')):
            valeurSoi.envoyer(bytes([30,2,1,0,0,0,0])); return
        if symboleTouche==0xffc3: valeurSoi.envoyer(bytes([30,2,2,0,0,0,0])); return
        if symboleTouche==0xffc9: valeurSoi.envoyer(bytes([30,2,3,0,0,0,0])); return
        if toucheContrôle and toucheDécaler and symboleTouche in (ord('v'), ord('V')):
            # Clipboard updates alone never execute text. An explicit paste key is required.
            valeurSoi.envoyer(valeurSoi.valeurPressePapiers); return
        toucheSpécial = {0xff08:b'\x7f',0xff09:b'\t',0xff0d:b'\r',0xff1b:b'\x1b',0xffff:b'\x1b[3~',
                   0xff50:b'\x1b[H',0xff57:b'\x1b[F',0xff51:b'\x1b[D',0xff52:b'\x1b[A',
                   0xff53:b'\x1b[C',0xff54:b'\x1b[B',0xff55:b'\x1b[5~',0xff56:b'\x1b[6~',0xffc9:b'\x1b[24~'}
        if symboleTouche in toucheSpécial: valeurSoi.envoyer(toucheSpécial[symboleTouche]); return
        encodageCaractère = symboleTouche & 0xffffff if symboleTouche & 0xff000000 == 0x01000000 else symboleTouche
        if encodageCaractère > 0x10ffff or 0xd800 <= encodageCaractère <= 0xdfff or symboleTouche >= 0xff00 and symboleTouche < 0x1000000: return
        if toucheContrôle and 0x40 <= encodageCaractère <= 0x7f: valeurSoi.envoyer(bytes([encodageCaractère & 31])); return
        if encodageCaractère < 32: return
        if valeurSoi.coréen and valeurSoi.toucheModificateur & {0xffea,0xfe03,0xff7e} and not toucheContrôle and hasattr(valeurSoi.ComposeurHangul, 'profile'):
            if valeurSoi.ComposeurHangul.toucheAlimenter(chr(encodageCaractère), altgr=True): return
        partiePréalable = b'\x1b' if valeurSoi.toucheModificateur & {0xffe9, 0xffea} else b''
        if valeurSoi.coréen and not toucheContrôle and not partiePréalable and 32<=encodageCaractère<127:
            donnéesCaractère=chr(encodageCaractère).upper() if toucheDécaler else chr(encodageCaractère)
            if valeurSoi.ComposeurHangul.toucheAlimenter(donnéesCaractère): return
        valeurSoi.envoyer(partiePréalable + chr(encodageCaractère).encode('utf-8'))


class connecterBureau:
    def __init__(valeurSoi, processus):
        valeurSoi.processus=processus; valeurSoi.valeurVerrou=threading.Lock(); valeurSoi.terminéPréparation=False; valeurSoi.terminal=False; valeurSoi.écranInitialValeur=False; valeurSoi.estFermé=False

    def envoyer(valeurSoi, Données):
        if not Données or valeurSoi.estFermé: return
        with valeurSoi.valeurVerrou:
            try: valeurSoi.processus.stdin.write(Données); valeurSoi.processus.stdin.flush()
            except (BrokenPipeError, ValueError): pass

    def entréeSortieSériel(valeurSoi):
        partieTerminaison=b''
        try:
            while True:
                Données=valeurSoi.processus.stdout.read(4096)
                if not Données: break
                sys.stdout.buffer.write(Données); sys.stdout.buffer.flush()
                partieTerminaison=(partieTerminaison+Données)[-8192:]
                ouvert=partieTerminaison.rfind(b'TERMINAL READY'); estFermé=partieTerminaison.rfind(b'TERMINAL CLOSED'); écranDessin=partieTerminaison.rfind(b'GUI READY:'); possèdeQuitté=partieTerminaison.rfind(b'GUI EXIT')
                # Preserve the mode after its marker has left the rolling UART buffer.
                if max(ouvert,estFermé,écranDessin,possèdeQuitté)>=0:
                    valeurSoi.terminal=ouvert>max(estFermé,écranDessin,possèdeQuitté)
                    valeurSoi.écranInitialValeur=écranDessin>max(ouvert,estFermé,possèdeQuitté)
                if not valeurSoi.terminéPréparation and b'jkoros-native> ' in partieTerminaison:
                    valeurSoi.terminéPréparation=True; valeurSoi.envoyer(b'terminal\n')
        finally: valeurSoi.estFermé=True

    def client(valeurSoi, client, chemin):
        valeurServeur=socket.socket(socket.AF_UNIX); valeurServeur.settimeout(10); client.settimeout(10)
        entréeÉlémentClavier=Clavier(valeurSoi.envoyer,lambda coréen:valeurSoi.envoyer(bytes([30,3,int(coréen),0,0,0,0])))
        boutonsPrécédentÉlément=0
        try:
            valeurServeur.connect(str(chemin))
            # étatValeurInitialValeur 협상은 순서대로 끝낸다. valeurAprès Sortie 가닥만 클라이언트에 쓴다.
            client.sendall(valeurExact(valeurServeur,12))
            numéroVersion=valeurExact(client,12)
            if numéroVersion not in (b'RFB 003.008\n',b'RFB 003.007\n'): raise ValueError('RFB 3.7/3.8 required')
            valeurServeur.sendall(numéroVersion)
            nombreÉlémentsÉlémentListe=valeurExact(valeurServeur,1);client.sendall(nombreÉlémentsÉlémentListe+valeurExact(valeurServeur,nombreÉlémentsÉlémentListe[0]))
            sécurité=valeurExact(client,1)
            if sécurité!=b'\x01': raise ValueError('unexpected security type')
            valeurServeur.sendall(sécurité)
            if numéroVersion==b'RFB 003.008\n':client.sendall(valeurExact(valeurServeur,4))
            valeurServeur.sendall(valeurExact(client,1))
            valeurInitialValeur=valeurExact(valeurServeur,24)
            client.sendall(valeurInitialValeur+valeurExact(valeurServeur,struct.unpack('>I',valeurInitialValeur[20:])[0]))
            octetsPixel=valeurInitialValeur[4]//8;prisEnChargePointeur=False
            client.settimeout(None);valeurServeur.settimeout(None)
            def sortie():
                try:
                    while True:
                        valeurCatégorie=valeurExact(valeurServeur,1)[0]
                        if valeurCatégorie==0:
                            valeurTête=valeurExact(valeurServeur,3);nombreÉlémentsEntréeÉlément=struct.unpack('>H',valeurTête[1:])[0]
                            # RFC 6143 §7.8.1: 커널이 그린 포인터와 valeurDistant 포인터의 중복을 피한다.
                            valeurCaché=prisEnChargePointeur
                            if valeurCaché:client.sendall(struct.pack('>BBHHHHHi',0,0,1,0,0,0,0,-239))
                            client.sendall(bytes([valeurCatégorie])+valeurTête)
                            for _ in range(nombreÉlémentsEntréeÉlément):
                                rectangle=valeurExact(valeurServeur,12);positionHorizontal,positionVertical,étendueLargeur,valeurHauteur,valeurEncodage=struct.unpack('>HHHHi',rectangle)
                                if valeurEncodage!=0:raise ValueError('unexpected framebuffer encoding: '+str(valeurEncodage))
                                client.sendall(rectangle)
                                donnéesResteDivision=étendueLargeur*valeurHauteur*octetsPixel
                                while donnéesResteDivision:
                                    Données=valeurExact(valeurServeur,min(donnéesResteDivision,65536));client.sendall(Données);donnéesResteDivision-=len(Données)
                        elif valeurCatégorie==1:
                            valeurTête=valeurExact(valeurServeur,5);nombreÉlémentsÉlémentListe=struct.unpack('>H',valeurTête[3:])[0]
                            client.sendall(bytes([valeurCatégorie])+valeurTête+valeurExact(valeurServeur,nombreÉlémentsÉlémentListe*6))
                        elif valeurCatégorie==2:client.sendall(bytes([valeurCatégorie]))
                        elif valeurCatégorie==3:
                            valeurTête=valeurExact(valeurServeur,7);nombreÉlémentsÉlémentListe=struct.unpack('>I',valeurTête[3:])[0]
                            if nombreÉlémentsÉlémentListe>1048576:raise ValueError('server clipboard too large')
                            client.sendall(bytes([valeurCatégorie])+valeurTête+valeurExact(valeurServeur,nombreÉlémentsÉlémentListe))
                        else:raise ValueError('unexpected RFB server message: '+str(valeurCatégorie))
                except (OSError,EOFError,ValueError):pass
                finally:
                    try:client.shutdown(socket.SHUT_RDWR)
                    except OSError:pass
            tâcheFond=threading.Thread(target=sortie,daemon=True);tâcheFond.start()
            while not valeurSoi.estFermé:
                valeurCatégorie=valeurExact(client,1)[0]
                if valeurCatégorie==4:
                    texteCorps=valeurExact(client,7); entréeÉlémentClavier.valeurEnfoncé(texteCorps[0]!=0,struct.unpack('>I',texteCorps[3:])[0]); continue
                if valeurCatégorie==255:
                    texteCorps=valeurExact(client,11)
                    if texteCorps[0]!=0: raise ValueError('unsupported QEMU input extension')
                    entréeÉlémentClavier.valeurEnfoncé(struct.unpack('>H',texteCorps[1:3])[0]!=0,struct.unpack('>I',texteCorps[3:7])[0]); continue
                if valeurCatégorie==5:
                    texteCorps=valeurExact(client,5); boutons,coordonnéeCoordonnéeHorizontale,coordonnéeCoordonnéeVerticale=struct.unpack('>BHH',texteCorps)
                    estEnfoncé=boutons&~boutonsPrécédentÉlément; boutonsPrécédentÉlément=boutons
                    if estEnfoncé: entréeÉlémentClavier.ComposeurHangul.compositionConfirmer()
                    if estEnfoncé&1 and valeurSoi.écranInitialValeur and 64<=coordonnéeCoordonnéeHorizontale<576 and 112<=coordonnéeCoordonnéeVerticale<372:
                        indiceRechercher=(coordonnéeCoordonnéeVerticale-112)//52
                        if (coordonnéeCoordonnéeVerticale-112)%52<40 and indiceRechercher<5: valeurSoi.envoyer(bytes([ord('1')+indiceRechercher]))
                    else: valeurSoi.envoyer(bytes([30,1,boutons,coordonnéeCoordonnéeHorizontale&255,coordonnéeCoordonnéeHorizontale>>8,coordonnéeCoordonnéeVerticale&255,coordonnéeCoordonnéeVerticale>>8]))
                    continue
                if valeurCatégorie==6:
                    texteCorps=valeurExact(client,7); longueur=struct.unpack('>i',texteCorps[3:])[0]
                    if abs(longueur)>65536: raise ValueError('clipboard too large')
                    texte=valeurExact(client,abs(longueur))
                    if longueur>=0:
                        try: entréeÉlémentClavier.valeurPressePapiers=texte.decode('utf-8').encode('utf-8')
                        except UnicodeDecodeError: entréeÉlémentClavier.valeurPressePapiers=texte.decode('latin-1').encode('utf-8')
                        entréeÉlémentClavier.valeurPressePapiers=entréeÉlémentClavier.valeurPressePapiers[:65536].decode('utf-8','ignore').encode('utf-8')
                    valeurServeur.sendall(bytes([valeurCatégorie])+texteCorps+texte); continue
                if valeurCatégorie==0:
                    texteCorps=valeurExact(client,19)
                    if texteCorps[3] not in (8,16,32):raise ValueError('unsupported pixel size')
                    octetsPixel=texteCorps[3]//8
                elif valeurCatégorie==2:
                    texteCorps=valeurExact(client,3); nombreÉlémentsEntréeÉlément=struct.unpack('>H',texteCorps[1:])[0]
                    if nombreÉlémentsEntréeÉlément>512: raise ValueError('too many encodings')
                    valeursEncodé=struct.unpack('>'+str(nombreÉlémentsEntréeÉlément)+'i',valeurExact(client,nombreÉlémentsEntréeÉlément*4))
                    prisEnChargePointeur=-239 in valeursEncodé
                    # 로컬 Écran 중계는 valeurDéfaut Raw만 요청하여 프레임 경계에서 포인터를 숨긴다.
                    texteCorps=struct.pack('>BHi',0,1,0)
                elif valeurCatégorie in (3,150): texteCorps=valeurExact(client,9)
                elif valeurCatégorie==248:
                    texteCorps=valeurExact(client,8)
                    if texteCorps[7]>64: raise ValueError('fence too large')
                    texteCorps+=valeurExact(client,texteCorps[7])
                elif valeurCatégorie==250: texteCorps=valeurExact(client,3)
                elif valeurCatégorie==251:
                    texteCorps=valeurExact(client,7)
                    if texteCorps[5]>16: raise ValueError('too many screens')
                    texteCorps+=valeurExact(client,texteCorps[5]*16)
                else: raise ValueError('unsupported RFB message {}'.format(valeurCatégorie))
                valeurServeur.sendall(bytes([valeurCatégorie])+texteCorps)
        except (OSError,EOFError,ValueError) as erreur:
            if str(erreur): print('VNC client:',erreur,file=sys.stderr,flush=True)
        finally:
            for valeurPriseRéseau in (client,valeurServeur):
                try: valeurPriseRéseau.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                valeurPriseRéseau.close()


def lancerBureau(numéroPort=5902, réseau=False, numéroPortTransfertFichier=2121, règlesTransfertEnCours=(), valeurRésolution=(640, 480), adresseInvité=None, adresseHôte='127.0.0.1'):
    with ExitStack() as ressources, tempfile.TemporaryDirectory(prefix='jkoros-desktop-') as cheminTravailEnCours:
        entréeÉlémentPontRéseau = None
        if réseau:
            from pontRéseau import pontRéseau
            entréeÉlémentPontRéseau = ressources.enter_context(pontRéseau(numéroPortTransfertFichier, règlesTransfertEnCours, adresseInvité=adresseInvité, adresseHôte=adresseHôte))
        chemin=Path(cheminTravailEnCours)/'display.sock'
        with socket.socket() as recevoirPort:
            recevoirPort.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            recevoirPort.bind(('127.0.0.1',numéroPort)); recevoirPort.listen(1); recevoirPort.settimeout(.2)
            portVNC=recevoirPort.getsockname()[1]
            if entréeÉlémentPontRéseau and (portVNC==numéroPortTransfertFichier or 50000<=portVNC<=50007 or any(ABIRéseau=='tcp' and Hôte==portVNC for ABIRéseau,Hôte,_ in entréeÉlémentPontRéseau.règlesTransfertEnCours)):
                raise ValueError('VNC port conflicts with an FTP/TCP forwarding port')
            processus=subprocess.Popen(commande(valeurRésolution)+['-display','none','-monitor','none','-serial','stdio','-vnc','unix:'+str(chemin)]+(entréeÉlémentPontRéseau.argumentTransféré() if entréeÉlémentPontRéseau else []),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
            pont=connecterBureau(processus); lecteur=threading.Thread(target=pont.entréeSortieSériel,daemon=True); lecteur.start()
            print('DESKTOP VNC 127.0.0.1:{} — Remmina VNC; keyboard/Unicode/paste bridge; Ctrl+C stops VM'.format(recevoirPort.getsockname()[1]),flush=True)
            if entréeÉlémentPontRéseau: print('NETWORK FTP {}:{} — guest command: ftpd start'.format(adresseHôte,numéroPortTransfertFichier),flush=True)
            def terminerProcessus(numéroSignal,cadreExécution): raise KeyboardInterrupt()
            précédentÉlément=signal.signal(signal.SIGTERM,terminerProcessus)
            tâcheTraitement=None; interrompu=False
            try:
                while processus.poll() is None:
                    try: client,_=recevoirPort.accept()
                    except socket.timeout: continue
                    if tâcheTraitement is not None and tâcheTraitement.is_alive(): client.close(); continue
                    if not chemin.exists(): client.close(); continue
                    tâcheTraitement=threading.Thread(target=pont.client,args=(client,chemin),daemon=True); tâcheTraitement.start()
            except KeyboardInterrupt: interrompu=True
            finally:
                pont.estFermé=True
                if entréeÉlémentPontRéseau: entréeÉlémentPontRéseau.évènementMettreEnPause.set()
                if processus.poll() is None:
                    processus.terminate()
                    try: processus.wait(timeout=5)
                    except subprocess.TimeoutExpired: processus.kill(); processus.wait()
                lecteur.join(timeout=2); processus.stdin.close(); processus.stdout.close(); signal.signal(signal.SIGTERM,précédentÉlément)
            if entréeÉlémentPontRéseau and entréeÉlémentPontRéseau.erreur: raise RuntimeError('network bridge: '+entréeÉlémentPontRéseau.erreur)
            return 0 if interrompu else processus.returncode


if __name__=='__main__':
    from exécuterCommande import lireRésolution
    analyseur=argparse.ArgumentParser(description=__doc__); analyseur.add_argument('--port',type=int,default=5902)
    analyseur.add_argument('--resolution',type=lireRésolution,default=(640,480))
    analyseur.add_argument('--network',action='store_true'); analyseur.add_argument('--ftp-port',type=int,default=2121)
    analyseur.add_argument('--forward',action='append',default=[])
    tableauArgument=analyseur.parse_args()
    if tableauArgument.forward and not tableauArgument.network: analyseur.error('--forward requires --network')
    raise SystemExit(lancerBureau(tableauArgument.port,réseau=tableauArgument.network,numéroPortTransfertFichier=tableauArgument.ftp_port,règlesTransfertEnCours=tableauArgument.forward,valeurRésolution=tableauArgument.resolution))
