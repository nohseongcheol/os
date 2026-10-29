// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Guyane_française.JGufOS.PileRéseau;

import java.util.HashMap;
import java.util.Map;

/** Centralise la répartition des réceptions Ethernet, ARP, IPv4, ICMP, UDP et TCP. */
public final class CoucheRéseau {
    @FunctionalInterface
    public interface gestionnaireÉvènementDonnées {
        void entréeÉlémentValeurProcessus(byte[] Données, int lancer, int longueur);
    }

    private final Map<Integer, gestionnaireÉvènementDonnées> GestionnaireÉvènementEthernet = new HashMap<Integer, gestionnaireÉvènementDonnées>();
    private final Map<Integer, gestionnaireÉvènementDonnées> GestionnaireÉvènementProtocoleInternet = new HashMap<Integer, gestionnaireÉvènementDonnées>();
    private final Map<Integer, gestionnaireÉvènementDonnées> gestionnaireÉvènementUnitéDonnéesUtilisateur = new HashMap<Integer, gestionnaireÉvènementDonnées>();
    private final Map<Integer, gestionnaireÉvènementDonnées> GestionnaireÉvènementContrôleTransmission = new HashMap<Integer, gestionnaireÉvènementDonnées>();

    public void registreEthernet(int valeurGenre, gestionnaireÉvènementDonnées GestionnaireÉvènement) {
        GestionnaireÉvènementEthernet.put(Integer.valueOf(valeurGenre & 0xffff), GestionnaireÉvènement);
    }

    public void registreProtocoleInternet(int valeurContrat, gestionnaireÉvènementDonnées GestionnaireÉvènement) {
        GestionnaireÉvènementProtocoleInternet.put(Integer.valueOf(valeurContrat & 0xff), GestionnaireÉvènement);
    }

    public void registreUnitéDonnéesUtilisateur(int portMatériel, gestionnaireÉvènementDonnées GestionnaireÉvènement) {
        gestionnaireÉvènementUnitéDonnéesUtilisateur.put(Integer.valueOf(portMatériel & 0xffff), GestionnaireÉvènement);
    }

    public void registreContrôleTransmission(int portMatériel, gestionnaireÉvènementDonnées GestionnaireÉvènement) {
        GestionnaireÉvènementContrôleTransmission.put(Integer.valueOf(portMatériel & 0xffff), GestionnaireÉvènement);
    }

    public boolean recevoirEthernet(byte[] indiceCadre) {
        if (!OutilsRéseau.estCadreEthernet(indiceCadre)) {
            return false;
        }
        int valeurGenre = OutilsRéseau.protocoleSupérieurEthernet(indiceCadre);
        gestionnaireÉvènementDonnées GestionnaireÉvènementDirect = GestionnaireÉvènementEthernet.get(Integer.valueOf(valeurGenre));
        if (GestionnaireÉvènementDirect != null) {
            GestionnaireÉvènementDirect.entréeÉlémentValeurProcessus(indiceCadre, 14, indiceCadre.length - 14);
            return true;
        }
        return valeurGenre == 0x0800 && recevoirPaquetInternet(indiceCadre, 14);
    }

    private boolean recevoirPaquetInternet(byte[] Données, int lancer) {
        if (!OutilsRéseau.estProtocole4VersionIP(Données, lancer)) {
            return false;
        }
        int longueurEntête = (Données[lancer] & 0x0f) * 4;
        int longueurTotal = OutilsRéseau.courtOrdreOctetsGrand(Données, lancer + 2);
        if (longueurTotal < longueurEntête || lancer + longueurTotal > Données.length) {
            return false;
        }
        int valeurContrat = Données[lancer + 9] & 0xff;
        int démarrerContenuValeur = lancer + longueurEntête;
        int longueurContenuValeur = longueurTotal - longueurEntête;
        gestionnaireÉvènementDonnées GestionnaireÉvènementDirect = GestionnaireÉvènementProtocoleInternet.get(Integer.valueOf(valeurContrat));
        if (GestionnaireÉvènementDirect != null) {
            GestionnaireÉvènementDirect.entréeÉlémentValeurProcessus(Données, démarrerContenuValeur, longueurContenuValeur);
            return true;
        }
        if (longueurContenuValeur < 4) {
            return false;
        }
        int numéroPortDestination = OutilsRéseau.courtOrdreOctetsGrand(Données, démarrerContenuValeur + 2);
        Map<Integer, gestionnaireÉvènementDonnées> tablePort = valeurContrat == 17 ? gestionnaireÉvènementUnitéDonnéesUtilisateur : valeurContrat == 6 ? GestionnaireÉvènementContrôleTransmission : null;
        if (tablePort == null) {
            return false;
        }
        gestionnaireÉvènementDonnées gestionnaireÉvènementPort = tablePort.get(Integer.valueOf(numéroPortDestination));
        if (gestionnaireÉvènementPort == null) {
            return false;
        }
        gestionnaireÉvènementPort.entréeÉlémentValeurProcessus(Données, démarrerContenuValeur, longueurContenuValeur);
        return true;
    }
}

