// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Wallis_et_Futuna.JWlfOS.SystèmeFichier;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Vérifie les en-têtes et segments de chargement des exécutables ELF32 petit-boutistes. */
public final class ChargeurCodeExécutable {
    public static final class valeurSection {
        private final int valeurGenre;
        private final int valeurDrapeau;
        private final int adresse;
        private final int positionFichier;
        private final int taille;

        valeurSection(int valeurGenre, int valeurDrapeau, int adresse, int positionFichier, int taille) {
            this.valeurGenre = valeurGenre;
            this.valeurDrapeau = valeurDrapeau;
            this.adresse = adresse;
            this.positionFichier = positionFichier;
            this.taille = taille;
        }

        public int valeurGenre() {
            return valeurGenre;
        }

        public int valeurDrapeau() {
            return valeurDrapeau;
        }

        public int adresse() {
            return adresse;
        }

        public int positionFichier() {
            return positionFichier;
        }

        public int taille() {
            return taille;
        }
    }

    public static final class image {
        private final int démarrerAdresse;
        private final List<valeurSection> listeSections;

        image(int démarrerAdresse, List<valeurSection> listeSections) {
            this.démarrerAdresse = démarrerAdresse;
            this.listeSections = Collections.unmodifiableList(listeSections);
        }

        public int démarrerAdresse() {
            return démarrerAdresse;
        }

        public List<valeurSection> listeSections() {
            return listeSections;
        }
    }

    public image Contrôles(byte[] Données) {
        if (Données == null || Données.length < 52
                || Données[0] != 0x7f || Données[1] != 'E' || Données[2] != 'L' || Données[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (Données[4] != 1 || Données[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int démarrerAdresse = analyserEntier(Données, 24);
        int positionTableSection = analyserEntier(Données, 32);
        int tailleEntréeÉlémentSection = lireEntierCourt(Données, 46);
        int nombreÉlémentsSection = lireEntierCourt(Données, 48);
        if (tailleEntréeÉlémentSection < 40 || positionTableSection < 0
                || (long) positionTableSection + (long) tailleEntréeÉlémentSection * nombreÉlémentsSection > Données.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<valeurSection> listeSections = new ArrayList<valeurSection>();
        for (int numéro = 0; numéro < nombreÉlémentsSection; numéro++) {
            int position = positionTableSection + numéro * tailleEntréeÉlémentSection;
            int valeurGenre = analyserEntier(Données, position + 4);
            int valeurDrapeau = analyserEntier(Données, position + 8);
            int adresse = analyserEntier(Données, position + 12);
            int positionFichier = analyserEntier(Données, position + 16);
            int taille = analyserEntier(Données, position + 20);
            if (taille < 0 || (valeurGenre != 8 && ((long) positionFichier + taille > Données.length || positionFichier < 0))) {
                throw new IllegalArgumentException("ELF valeurSection Données 범위가 올바르지 않습니다.");
            }
            listeSections.add(new valeurSection(valeurGenre, valeurDrapeau, adresse, positionFichier, taille));
        }
        return new image(démarrerAdresse, listeSections);
    }

    private int analyserEntier(byte[] Données, int position) {
        if (position < 0 || position > Données.length - 4) {
            throw new IllegalArgumentException("ELF Entier 범위를 벗어났습니다.");
        }
        return (Données[position] & 0xff)
                | ((Données[position + 1] & 0xff) << 8)
                | ((Données[position + 2] & 0xff) << 16)
                | ((Données[position + 3] & 0xff) << 24);
    }

    private int lireEntierCourt(byte[] Données, int position) {
        if (position < 0 || position > Données.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 Entier 범위를 벗어났습니다.");
        }
        return (Données[position] & 0xff) | ((Données[position + 1] & 0xff) << 8);
    }
}
