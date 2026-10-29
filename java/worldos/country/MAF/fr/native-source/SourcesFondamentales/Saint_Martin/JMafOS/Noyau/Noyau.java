// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Saint_Martin.JMafOS.Noyau;

import Saint_Martin.JMafOS.EspaceMémoire.GestionnaireMémoire;
import Saint_Martin.JMafOS.EspaceMémoire.GestionnairePage;
import Saint_Martin.JMafOS.valeurEntrée.GestionnaireEntrée;
import Saint_Martin.JMafOS.Tâche.valeurProcessus;
import Saint_Martin.JMafOS.Tâche.Ordonnanceur;
import Saint_Martin.JMafOS.AppelSystème.AppelSystème;
import Saint_Martin.JMafOS.SystèmeFichier.tableDescripteurFichier;
import Saint_Martin.JMafOS.SystèmeFichier.SystèmeFichier;

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
        Périphérique.sortieSériel("=== JMafOS 관리 valeurNoyau ===\n");
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
