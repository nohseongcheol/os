// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Wallis_et_Futuna.JWlfOS.Périphérique;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Gère les résultats de détection PCI et les valeurs BAR/IRQ. */
public final class GestionnaireBusPériphériqueMatériel {
    public static final class Périphérique {
        private final int identificateurFournisseur;
        private final int identificateurPériphérique;
        private final int baseEntréeSortie;
        private final int numéroInterrompre;

        public Périphérique(int identificateurFournisseur, int identificateurPériphérique, int baseEntréeSortie, int numéroInterrompre) {
            this.identificateurFournisseur = identificateurFournisseur;
            this.identificateurPériphérique = identificateurPériphérique;
            this.baseEntréeSortie = baseEntréeSortie;
            this.numéroInterrompre = numéroInterrompre;
        }

        public int identificateurFournisseur() { return identificateurFournisseur; }
        public int identificateurPériphérique() { return identificateurPériphérique; }
        public int baseEntréeSortie() { return baseEntréeSortie; }
        public int numéroInterrompre() { return numéroInterrompre; }
    }

    private final List<Périphérique> listePériphériques = new ArrayList<Périphérique>();

    public void valeurDécouvert(Périphérique Périphérique) {
        listePériphériques.add(Périphérique);
    }

    public List<Périphérique> listePériphériques() {
        return Collections.unmodifiableList(listePériphériques);
    }

    public Périphérique trouverEntréeÉlément(int identificateurFournisseur, int identificateurPériphérique) {
        for (Périphérique candidat : listePériphériques) {
            if (candidat.identificateurFournisseur == identificateurFournisseur && candidat.identificateurPériphérique == identificateurPériphérique) {
                return candidat;
            }
        }
        return null;
    }
}

