// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suisse.JCheOS.Noyau;

import Suisse.JCheOS.EspaceMémoire.GestionnaireMémoire;
import Suisse.JCheOS.EspaceMémoire.GestionnairePage;
import Suisse.JCheOS.valeurEntrée.GestionnaireEntrée;
import Suisse.JCheOS.Tâche.valeurProcessus;
import Suisse.JCheOS.Tâche.Ordonnanceur;
import Suisse.JCheOS.AppelSystème.AppelSystème;
import Suisse.JCheOS.SystèmeFichier.tableDescripteurFichier;
import Suisse.JCheOS.SystèmeFichier.SystèmeFichier;

/** Assemble et démarre le noyau géré en Java. */
public final class Noyau {
    private final valeurMatériel Périphérique;
    private final GestionnaireMémoire EspaceMémoire = new GestionnaireMémoire(32 * 1024 * 1024);
    private final GestionnairePage gestionPage = new GestionnairePage();
    private final SystèmeFichier SystèmeFichier = new SystèmeFichier();
    private final Ordonnanceur Ordonnanceur = new Ordonnanceur(gestionPage);
    private final GestionnaireEntrée GestionEntrée = new GestionnaireEntrée(256);
    private final valeurProcessus processusPremier;
    private final AppelSystème AppelSystème;

    public Noyau(valeurMatériel Périphérique) {
        this.Périphérique = Périphérique;
        processusPremier = Ordonnanceur.processusPremier(new tableDescripteurFichier(SystèmeFichier));
        AppelSystème = new AppelSystème(SystèmeFichier, gestionPage, Ordonnanceur, Périphérique, GestionEntrée);
    }

    public void lancer() {
        Périphérique.sortieSériel("=== JCheOS 관리 valeurNoyau ===\n");
    }

    public void exécuterÉtape() {
        Périphérique.cPUArrêterMachine();
    }

    public GestionnaireMémoire EspaceMémoire() {
        return EspaceMémoire;
    }

    public GestionnairePage gestionPage() {
        return gestionPage;
    }

    public SystèmeFichier SystèmeFichier() {
        return SystèmeFichier;
    }

    public Ordonnanceur Ordonnanceur() {
        return Ordonnanceur;
    }

    public GestionnaireEntrée GestionEntrée() {
        return GestionEntrée;
    }

    public valeurProcessus processusPremier() {
        return processusPremier;
    }

    public AppelSystème AppelSystème() {
        return AppelSystème;
    }
}
