// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italie.JItaOS.Tâche;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Italie.JItaOS.EspaceMémoire.GestionnairePage;
import Italie.JItaOS.SystèmeFichier.tableDescripteurFichier;

/** Gère les identifiants de processus et une file des prêts à tour de rôle. */
public final class Ordonnanceur {
    private final GestionnairePage gestionPage;
    private final Map<Integer, valeurProcessus> listeProcessus = new HashMap<Integer, valeurProcessus>();
    private final Queue<valeurProcessus> fileAttentePrêt = new ArrayDeque<valeurProcessus>();
    private int identificateurSuivant = 1;

    public Ordonnanceur(GestionnairePage gestionPage) {
        this.gestionPage = gestionPage;
    }

    public valeurProcessus processusPremier(tableDescripteurFichier descripteurFichier) {
        valeurProcessus processusNouveau = new valeurProcessus(allouerIdentificateur(), 0, gestionPage.espaceAdresseNouveau(), descripteurFichier);
        listeProcessus.put(Integer.valueOf(processusNouveau.valeurIdentificateur()), processusNouveau);
        fileAttentePrêt.offer(processusNouveau);
        return processusNouveau;
    }

    public valeurProcessus valeurCloner(valeurProcessus valeurParent) {
        valeurProcessus valeurEnfant = new valeurProcessus(
                allouerIdentificateur(),
                valeurParent.valeurIdentificateur(),
                gestionPage.écrireActivéCopierCloner(valeurParent.EspaceAdresse()),
                valeurParent.descripteurFichier().valeurCloner());
        valeurEnfant.définirRompreProgramme(valeurParent.rompreProgramme());
        listeProcessus.put(Integer.valueOf(valeurEnfant.valeurIdentificateur()), valeurEnfant);
        fileAttentePrêt.offer(valeurEnfant);
        return valeurEnfant;
    }

    public valeurProcessus processusSuivant() {
        int contrôlerNombreÉléments = fileAttentePrêt.size();
        for (int numéro = 0; numéro < contrôlerNombreÉléments; numéro++) {
            valeurProcessus élémentListeSuivant = fileAttentePrêt.poll();
            if (élémentListeSuivant != null && (élémentListeSuivant.valeurÉtatValeur() == étatValeurProcessus.préparer || élémentListeSuivant.valeurÉtatValeur() == étatValeurProcessus.exécuterCommande)) {
                élémentListeSuivant.définirÉtatValeur(étatValeurProcessus.exécuterCommande);
                fileAttentePrêt.offer(élémentListeSuivant);
                return élémentListeSuivant;
            }
        }
        return null;
    }

    public int attendreEnfantPour(valeurProcessus valeurParent, int identificateurEnfant, boolean bloquantNon) {
        for (valeurProcessus candidat : listeProcessus.values()) {
            if (candidat.identificateurParent() != valeurParent.valeurIdentificateur()) {
                continue;
            }
            if (identificateurEnfant > 0 && candidat.valeurIdentificateur() != identificateurEnfant) {
                continue;
            }
            if (candidat.valeurÉtatValeur() == étatValeurProcessus.programmeQuitter) {
                int résultat = (candidat.codeQuitter() & 0xff) << 8;
                listeProcessus.remove(Integer.valueOf(candidat.valeurIdentificateur()));
                return résultat;
            }
            return bloquantNon ? 0 : -11;
        }
        return -10;
    }

    public valeurProcessus trouverProcessus(int valeurIdentificateur) {
        return listeProcessus.get(Integer.valueOf(valeurIdentificateur));
    }

    private int allouerIdentificateur() {
        return identificateurSuivant++;
    }
}
