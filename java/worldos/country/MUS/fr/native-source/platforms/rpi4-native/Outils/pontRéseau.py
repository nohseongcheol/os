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

adresseMachine = bytes.fromhex('525400123456')
adresseMatérielPasserelle = bytes.fromhex('52550a000202')
valeurAdresseInternet = ipaddress.IPv4Address(read_config(Path(__file__).resolve().parents[1])['IP']).packed


class pontRéseau:
    def __init__(valeurSoi, numéroPortTransfertFichier=2121, règlesTransfertEnCours=(), capturer=False, adresseInvité=None, adresseHôte='127.0.0.1'):
        if not 1024 <= numéroPortTransfertFichier <= 65535 or 50000 <= numéroPortTransfertFichier <= 50007:
            raise ValueError('FTP host port must be 1024..65535 excluding 50000..50007')
        valeurSoi.numéroPortTransfertFichier = numéroPortTransfertFichier
        valeurSoi.ip_config = read_config(Path(__file__).resolve().parents[1])
        adresseInvité = adresseInvité or valeurSoi.ip_config['IP']
        qemu_network(valeurSoi.ip_config, adresseInvité)
        adresse=ipaddress.IPv4Address(adresseInvité)
        valeurSoi.adresseInvité=str(adresse); valeurSoi.adresseActuel=adresse.packed
        adresse=ipaddress.IPv4Address(adresseHôte)
        if adresse.is_multicast or str(adresse)=='255.255.255.255':raise ValueError('Network forwarding host must be a unicast IPv4 address or 0.0.0.0')
        valeurSoi.adresseHôte=str(adresse)
        valeurSoi.capturer = capturer; valeurSoi.journalTrace = []
        valeurSoi.règlesTransfertEnCours = []
        occupé = {('tcp', numéroPortTransfertFichier)} | {('tcp', positionDonnées) for positionDonnées in range(50000,50008)}
        for valeurRègle in règlesTransfertEnCours:
            composantChemin = valeurRègle.split(':')
            if len(composantChemin) != 3 or composantChemin[0] not in ('tcp', 'udp'):
                raise ValueError('forward must be tcp:HOST_PORT:GUEST_PORT or udp:HOST_PORT:GUEST_PORT')
            ABIRéseau, Hôte, invité = composantChemin[0], int(composantChemin[1]), int(composantChemin[2])
            if not 1024 <= Hôte <= 65535 or not 1 <= invité <= 65535 or (ABIRéseau, Hôte) in occupé:
                raise ValueError('invalid or duplicate forward: ' + valeurRègle)
            occupé.add((ABIRéseau, Hôte)); valeurSoi.règlesTransfertEnCours.append((ABIRéseau, Hôte, invité))
        valeurSoi.recevoirPorts = []
        for _ in range(2):
            valeurServeur = socket.socket()
            valeurServeur.bind(('127.0.0.1', 0)); valeurServeur.listen(1); valeurServeur.setblocking(False)
            valeurSoi.recevoirPorts.append(valeurServeur)
        valeurSoi.clients = [None, None]
        valeurSoi.estEnAttente = [bytearray(), bytearray()]
        valeurSoi.ethernet = bytearray(); valeurSoi.datagrammeSériel = bytearray(); valeurSoi.échappé = valeurSoi.estInvalide = False
        valeurSoi.évènementMettreEnPause = threading.Event(); valeurSoi.erreur = None
        valeurSoi.invitéVersCadres = valeurSoi.invitéDepuisCadres = 0
        valeurSoi.tâcheFond = threading.Thread(target=valeurSoi.valeurCycle, daemon=True)
        valeurSoi.tâcheFond.start()

    def argumentTransféré(valeurSoi):
        numéroPortSériel, portEthernet = [donnéesChaîne.getsockname()[1] for donnéesChaîne in valeurSoi.recevoirPorts]
        règleTransfertEnCours = 'user,id=wan,' + qemu_network(valeurSoi.ip_config, valeurSoi.adresseInvité) + ',hostfwd=tcp:127.0.0.1:{}-{}:21'.format(valeurSoi.numéroPortTransfertFichier, valeurSoi.adresseInvité)
        for numéroPort in range(50000, 50008):
            règleTransfertEnCours += ',hostfwd=tcp:127.0.0.1:{0}-{1}:{0}'.format(numéroPort, valeurSoi.adresseInvité)
        for ABIRéseau, Hôte, invité in valeurSoi.règlesTransfertEnCours:
            règleTransfertEnCours += ',hostfwd={}:127.0.0.1:{}-{}:{}'.format(ABIRéseau, Hôte, valeurSoi.adresseInvité, invité)
        règleTransfertEnCours=règleTransfertEnCours.replace('127.0.0.1:',valeurSoi.adresseHôte+':')
        return ['-chardev', 'socket,id=slip,host=127.0.0.1,port={}'.format(numéroPortSériel),
                '-serial', 'chardev:slip', '-netdev', règleTransfertEnCours,
                '-netdev', 'socket,id=wire,connect=127.0.0.1:{}'.format(portEthernet),
                '-netdev', 'hubport,id=wanhub,hubid=0,netdev=wan',
                '-netdev', 'hubport,id=wirehub,hubid=0,netdev=wire']

    def cadreExécution(valeurSoi, donnéesPaquet):
        valeurSoi.estEnAttente[1] += struct.pack('!I', len(donnéesPaquet)) + donnéesPaquet

    def paquetTrace(valeurSoi, direction, donnéesPaquet):
        if not valeurSoi.capturer or len(donnéesPaquet)<20: return
        valeurDécalage=(donnéesPaquet[0]&15)*4
        valeurEntréeÉlément={'time':time.monotonic(),'direction':direction,'bytes':len(donnéesPaquet),'protocol':donnéesPaquet[9]}
        if donnéesPaquet[9]==6 and len(donnéesPaquet)>=valeurDécalage+20:
            donnéesOriginal,adresseDonnéesDestination,numéroOrdre,numéroConfirmation,bitsConfiguration,fenêtre=struct.unpack_from('!HHIIHH',donnéesPaquet,valeurDécalage)
            valeurEntréeÉlément.update(source=donnéesOriginal,destination=adresseDonnéesDestination,seq=numéroOrdre,ack=numéroConfirmation,flags=bitsConfiguration&255,window=fenêtre,
                        payload=len(donnéesPaquet)-valeurDécalage-((donnéesPaquet[valeurDécalage+12]>>4)*4))
        valeurSoi.journalTrace.append(valeurEntréeÉlément)
        if len(valeurSoi.journalTrace)>2048: del valeurSoi.journalTrace[:1024]

    def entréeSLIP(valeurSoi, Données):
        for codeCaractère in Données:
            if codeCaractère == 192:
                if valeurSoi.datagrammeSériel and not valeurSoi.estInvalide and not valeurSoi.échappé:
                    # Learn the actual SLIP source after guest ipconfig changes.
                    # The bridge still only answers ARP for one current address.
                    if len(valeurSoi.datagrammeSériel)>=20 and valeurSoi.datagrammeSériel[0]>>4==4:
                        adresse=bytes(valeurSoi.datagrammeSériel[12:16])
                        try:
                            qemu_network(valeurSoi.ip_config, str(ipaddress.IPv4Address(adresse)))
                            valeurSoi.adresseActuel=adresse
                        except ValueError:
                            pass
                    valeurSoi.paquetTrace('from_guest',valeurSoi.datagrammeSériel)
                    valeurSoi.cadreExécution(adresseMatérielPasserelle + adresseMachine + b'\x08\x00' + valeurSoi.datagrammeSériel)
                    valeurSoi.invitéDepuisCadres += 1
                valeurSoi.datagrammeSériel.clear(); valeurSoi.échappé = valeurSoi.estInvalide = False
            elif codeCaractère == 219 and not valeurSoi.échappé:
                valeurSoi.échappé = True
            else:
                if valeurSoi.échappé:
                    if codeCaractère not in (220, 221): valeurSoi.estInvalide = True
                    codeCaractère = 192 if codeCaractère == 220 else 219
                    valeurSoi.échappé = False
                if len(valeurSoi.datagrammeSériel) < 1600: valeurSoi.datagrammeSériel.append(codeCaractère)
                else: valeurSoi.estInvalide = True

    def entréeEthernet(valeurSoi, Données):
        valeurSoi.ethernet += Données
        while len(valeurSoi.ethernet) >= 4:
            nombreÉlémentsÉlémentListe = struct.unpack_from('!I', valeurSoi.ethernet)[0]
            if nombreÉlémentsÉlémentListe > 65536: raise ValueError('oversized QEMU Ethernet frame')
            if len(valeurSoi.ethernet) < nombreÉlémentsÉlémentListe + 4: return
            cadreExécution = bytes(valeurSoi.ethernet[4:4+nombreÉlémentsÉlémentListe]); del valeurSoi.ethernet[:4+nombreÉlémentsÉlémentListe]
            if len(cadreExécution) < 14: continue
            if cadreExécution[12:14] == b'\x08\x06' and len(cadreExécution) >= 42:
                paquetRésolutionAdresse = cadreExécution[14:42]
                if paquetRésolutionAdresse[:8] == b'\x00\x01\x08\x00\x06\x04\x00\x01' and paquetRésolutionAdresse[24:28] == valeurSoi.adresseActuel:
                    réponseRetour = paquetRésolutionAdresse[:6] + b'\x00\x02' + adresseMachine + valeurSoi.adresseActuel + paquetRésolutionAdresse[8:18]
                    valeurSoi.cadreExécution(cadreExécution[6:12] + adresseMachine + b'\x08\x06' + réponseRetour)
            elif cadreExécution[12:14] == b'\x08\x00':
                donnéesPaquet = cadreExécution[14:]
                valeurSoi.paquetTrace('to_guest',donnéesPaquet)
                valeurSoi.estEnAttente[0] += b'\xc0' + donnéesPaquet.replace(b'\xdb', b'\xdb\xdd').replace(b'\xc0', b'\xdb\xdc') + b'\xc0'
                valeurSoi.invitéVersCadres += 1

    def valeurCycle(valeurSoi):
        try:
            while not valeurSoi.évènementMettreEnPause.is_set():
                lecteurs = [donnéesChaîne for indiceOrdinal, donnéesChaîne in enumerate(valeurSoi.recevoirPorts) if valeurSoi.clients[indiceOrdinal] is None]
                lecteurs += [donnéesChaîne for donnéesChaîne in valeurSoi.clients if donnéesChaîne is not None]
                rédacteurs = [donnéesChaîne for indiceOrdinal, donnéesChaîne in enumerate(valeurSoi.clients) if donnéesChaîne is not None and valeurSoi.estEnAttente[indiceOrdinal]]
                peutLire, inscriptible, _ = select.select(lecteurs, rédacteurs, [], .05)
                for donnéesChaîne in peutLire:
                    if donnéesChaîne in valeurSoi.recevoirPorts:
                        indiceOrdinal = valeurSoi.recevoirPorts.index(donnéesChaîne); valeurSoi.clients[indiceOrdinal], _ = donnéesChaîne.accept(); valeurSoi.clients[indiceOrdinal].setblocking(False)
                    else:
                        indiceOrdinal = valeurSoi.clients.index(donnéesChaîne); Données = donnéesChaîne.recv(16384)
                        if not Données: return
                        (valeurSoi.entréeSLIP if indiceOrdinal == 0 else valeurSoi.entréeEthernet)(Données)
                for donnéesChaîne in inscriptible:
                    indiceOrdinal = valeurSoi.clients.index(donnéesChaîne)
                    try: nombreÉlémentsÉlémentListe = donnéesChaîne.send(valeurSoi.estEnAttente[indiceOrdinal])
                    except BlockingIOError: continue
                    del valeurSoi.estEnAttente[indiceOrdinal][:nombreÉlémentsÉlémentListe]
                if any(len(valeurDeuxième) > 1024 * 1024 for valeurDeuxième in valeurSoi.estEnAttente):
                    raise RuntimeError('SLIP bridge queue exhausted')
        except Exception as entréeÉlémentAuxiliaire:
            if not valeurSoi.évènementMettreEnPause.is_set(): valeurSoi.erreur = str(entréeÉlémentAuxiliaire)

    def fermer(valeurSoi):
        valeurSoi.évènementMettreEnPause.set(); valeurSoi.tâcheFond.join(timeout=2)
        for donnéesChaîne in valeurSoi.recevoirPorts + valeurSoi.clients:
            if donnéesChaîne is not None: donnéesChaîne.close()

    def __enter__(valeurSoi): return valeurSoi
    def __exit__(valeurSoi, *tableauArgument): valeurSoi.fermer()
