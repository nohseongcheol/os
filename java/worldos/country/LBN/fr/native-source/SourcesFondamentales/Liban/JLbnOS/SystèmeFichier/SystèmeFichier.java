// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Liban.JLbnOS.SystèmeFichier;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** Modèle géré d’un stockage de fichiers en lecture seule correspondant à la couche de lecture FAT d’engos. */
public final class SystèmeFichier {
    static final class fichierOuvert {
        final byte[] Données;
        int position;
        int nombreÉlémentsRéférence = 1;

        fichierOuvert(byte[] Données) {
            this.Données = Données;
        }
    }

    private final Map<String, byte[]> entréesListeFichier = new LinkedHashMap<String, byte[]>();

    public void ajouterFinFichier(String nom, byte[] Données) {
        entréesListeFichier.put(nomCanonique(nom), Arrays.copyOf(Données, Données.length));
    }

    fichierOuvert ouvrir(String nom) {
        byte[] Données = entréesListeFichier.get(nomCanonique(nom));
        if (Données == null) {
            return null;
        }
        return new fichierOuvert(Données);
    }

    public boolean valeurExiste(String nom) {
        return entréesListeFichier.containsKey(nomCanonique(nom));
    }

    public informationFichier informationSystème(String nom) {
        byte[] Données = entréesListeFichier.get(nomCanonique(nom));
        if (Données == null) {
            return null;
        }
        return new informationFichier(Données.length, 0100444);
    }

    private String nomCanonique(String nom) {
        if (nom == null) {
            throw new NullPointerException("Fichier 이름이 없습니다.");
        }
        String résultat = nom.startsWith("/") ? nom.substring(1) : nom;
        return résultat.toUpperCase(Locale.ROOT);
    }
}
