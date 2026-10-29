"""Independent host TCP/UDP echo peers for native network integration tests."""
import socket
import threading


class DispositifTestRépercuter:
    def __enter__(valeurSoi):
        valeurSoi.contrôleConnexion = socket.socket(); valeurSoi.contrôleConnexion.bind(('127.0.0.1', 0)); valeurSoi.contrôleConnexion.listen(1)
        valeurSoi.contrôleDatagramme = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); valeurSoi.contrôleDatagramme.bind(('127.0.0.1', 0))
        valeurSoi.contrôleConnexion.settimeout(30); valeurSoi.contrôleDatagramme.settimeout(30)
        valeurSoi.portTCP = valeurSoi.contrôleConnexion.getsockname()[1]; valeurSoi.portUDP = valeurSoi.contrôleDatagramme.getsockname()[1]
        valeurSoi.erreurs = []; valeurSoi.possèdeReçu = {}
        def contrôleConnexion():
            try:
                connexion, _ = valeurSoi.contrôleConnexion.accept()
                with connexion:
                    connexion.settimeout(5); Données = bytearray()
                    while b'\n' not in Données:
                        valeurFragment = connexion.recv(512)
                        if not valeurFragment: raise RuntimeError('TCP EOF before request')
                        Données.extend(valeurFragment)
                    valeurSoi.possèdeReçu['tcp'] = bytes(Données); connexion.sendall(Données)
            except Exception as entréeÉlémentAuxiliaire: valeurSoi.erreurs.append(str(entréeÉlémentAuxiliaire))
        def contrôleDatagramme():
            try:
                Données, valeurPairRéseau = valeurSoi.contrôleDatagramme.recvfrom(512); valeurSoi.possèdeReçu['udp'] = Données; valeurSoi.contrôleDatagramme.sendto(Données, valeurPairRéseau)
            except Exception as entréeÉlémentAuxiliaire: valeurSoi.erreurs.append(str(entréeÉlémentAuxiliaire))
        valeurSoi.filsExécution = [threading.Thread(target=entréeÉlémentFichier, daemon=True) for entréeÉlémentFichier in (contrôleConnexion, contrôleDatagramme)]
        for entréeÉlémentTerminal in valeurSoi.filsExécution: entréeÉlémentTerminal.start()
        return valeurSoi

    def __exit__(valeurSoi, *tableauArgument):
        valeurSoi.contrôleConnexion.close(); valeurSoi.contrôleDatagramme.close()
        for entréeÉlémentTerminal in valeurSoi.filsExécution: entréeÉlémentTerminal.join(timeout=1)
