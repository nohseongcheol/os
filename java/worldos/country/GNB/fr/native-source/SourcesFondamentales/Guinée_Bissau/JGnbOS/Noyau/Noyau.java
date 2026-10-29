// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Guinée_Bissau.JGnbOS.Noyau;

import Guinée_Bissau.JGnbOS.EspaceMémoire.GestionnaireMémoire;
import Guinée_Bissau.JGnbOS.EspaceMémoire.GestionnairePage;
import Guinée_Bissau.JGnbOS.valeurEntrée.GestionnaireEntrée;
import Guinée_Bissau.JGnbOS.Tâche.valeurProcessus;
import Guinée_Bissau.JGnbOS.Tâche.Ordonnanceur;
import Guinée_Bissau.JGnbOS.AppelSystème.AppelSystème;
import Guinée_Bissau.JGnbOS.SystèmeFichier.tableDescripteurFichier;
import Guinée_Bissau.JGnbOS.SystèmeFichier.SystèmeFichier;

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
        Périphérique.sortieSériel("=== JGnbOS 관리 valeurNoyau ===\n");
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
