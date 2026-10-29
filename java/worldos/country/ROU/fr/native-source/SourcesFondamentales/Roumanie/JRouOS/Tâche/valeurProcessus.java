// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Roumanie.JRouOS.Tâche;

import Roumanie.JRouOS.EspaceMémoire.GestionnairePage;
import Roumanie.JRouOS.SystèmeFichier.tableDescripteurFichier;

public final class valeurProcessus {
    private final int valeurIdentificateur;
    private final int identificateurParent;
    private final GestionnairePage.EspaceAdresse EspaceAdresse;
    private final tableDescripteurFichier descripteurFichier;
    private étatValeurProcessus valeurÉtatValeur = étatValeurProcessus.préparer;
    private int codeQuitter;
    private int rompreProgramme = 0x06000000;
    private int adresseDémarrerExécution;
    private String[] argumentExécution = new String[0];
    private String[] valeurEnvironnement = new String[0];

    valeurProcessus(int valeurIdentificateur, int identificateurParent, GestionnairePage.EspaceAdresse EspaceAdresse, tableDescripteurFichier descripteurFichier) {
        this.valeurIdentificateur = valeurIdentificateur;
        this.identificateurParent = identificateurParent;
        this.EspaceAdresse = EspaceAdresse;
        this.descripteurFichier = descripteurFichier;
    }

    public int valeurIdentificateur() {
        return valeurIdentificateur;
    }

    public int identificateurParent() {
        return identificateurParent;
    }

    public GestionnairePage.EspaceAdresse EspaceAdresse() {
        return EspaceAdresse;
    }

    public tableDescripteurFichier descripteurFichier() {
        return descripteurFichier;
    }

    public étatValeurProcessus valeurÉtatValeur() {
        return valeurÉtatValeur;
    }

    public void définirÉtatValeur(étatValeurProcessus étatValeurNouveau) {
        valeurÉtatValeur = étatValeurNouveau;
    }

    public int codeQuitter() {
        return codeQuitter;
    }

    public void programmeQuitter(int valeur) {
        codeQuitter = valeur & 0xff;
        valeurÉtatValeur = étatValeurProcessus.programmeQuitter;
    }

    public int rompreProgramme() {
        return rompreProgramme;
    }

    public void définirRompreProgramme(int finNouveau) {
        if (finNouveau < 0x06000000 || finNouveau > 0x07000000) {
            throw new IllegalArgumentException("Programme terminaison 범위를 벗어났습니다.");
        }
        rompreProgramme = finNouveau;
    }

    public void définirContexteExécution(int démarrerAdresse, String[] argumentParamètre, String[] environnement) {
        adresseDémarrerExécution = démarrerAdresse;
        argumentExécution = argumentParamètre.clone();
        valeurEnvironnement = environnement.clone();
    }

    public int adresseDémarrerExécution() { return adresseDémarrerExécution; }
    public String[] argumentExécution() { return argumentExécution.clone(); }
    public String[] valeurEnvironnement() { return valeurEnvironnement.clone(); }
}
