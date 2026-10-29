// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import français.interne.Connexion;
import français.interne.Arguments;
import français.interne.CanalDatagramme;
import français.interne.Caractères;
import français.interne.Sortie;
import français.interne.Contrôles;
import français.interne.FluxEntrée;
import français.interne.ExceptionSortieEntrée;

public class ExempleRéseau {
    public static void lancer() throws ExceptionSortieEntrée {
        // Hôte : python3 Outils/répercuterExemple.py --tcp-port 9000 --udp-port 9001
        Connexion connecter = Connexion.ouvrir("10.0.2.2", Caractères.analyserEntier(Arguments.texte(0)));
        try {
            connecter.délaiExpiration(700);
            byte[] message = Caractères.encoder("JAVA TCP fr\n");
            connecter.Sortie().écrire(message);
            FluxEntrée valeurEntrée = connecter.valeurEntrée();
            for (int nombre = 0; nombre < Caractères.nombreÉlémentsOctet(message); nombre++) {
                Contrôles.exiger(valeurEntrée.lire() == (message[nombre] & 255), "TCP réponse 불일치");
            }
        } finally { connecter.fermer(); }
        CanalDatagramme extrémité = CanalDatagramme.ouvrir(0);
        try {
            extrémité.délaiExpiration(700);
            extrémité.envoyer("10.0.2.2", Caractères.analyserEntier(Arguments.texte(1)), "JAVA UDP fr");
            Contrôles.exiger(Caractères.texteÉgal(extrémité.recevoir(), "JAVA UDP fr"), "UDP réponse 불일치");
        } finally { extrémité.fermer(); }
        Sortie.écrireLigne("JAVA 네트워크 vérifier: TCP UDP fr");
    }
}
