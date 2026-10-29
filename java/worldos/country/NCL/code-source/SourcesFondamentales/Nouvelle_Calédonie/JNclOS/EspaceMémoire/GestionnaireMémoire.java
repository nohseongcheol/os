// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nouvelle_Calédonie.JNclOS.EspaceMémoire;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** Assure l’allocation alignée, la libération et la fusion des zones de mémoire physique. */
public final class GestionnaireMémoire {
    private final byte[] EspaceMémoire;
    private final TreeMap<Integer, Integer> régionVide = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> régionUtilisé = new TreeMap<Integer, Integer>();

    public GestionnaireMémoire(int tailleTotal) {
        if (tailleTotal < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        EspaceMémoire = new byte[tailleTotal];
        régionVide.put(Integer.valueOf(4096), Integer.valueOf(tailleTotal - 4096));
    }

    public synchronized int allouerStockage(int taille) {
        return allouerAligné(taille, 1);
    }

    public synchronized int allouerAligné(int taille, int valeurAligner) {
        if (taille <= 0 || valeurAligner <= 0 || (valeurAligner & (valeurAligner - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> valeurEntréeÉlément : régionVide.entrySet()) {
            int lancer = valeurEntréeÉlément.getKey().intValue();
            int tailleRégion = valeurEntréeÉlément.getValue().intValue();
            int démarrerAligné = (lancer + valeurAligner - 1) & -valeurAligner;
            int tailleValeurAvantCôté = démarrerAligné - lancer;
            int tailleFinal = tailleRégion - tailleValeurAvantCôté - taille;
            if (tailleFinal < 0) {
                continue;
            }
            régionVide.remove(Integer.valueOf(lancer));
            if (tailleValeurAvantCôté > 0) {
                régionVide.put(Integer.valueOf(lancer), Integer.valueOf(tailleValeurAvantCôté));
            }
            if (tailleFinal > 0) {
                régionVide.put(Integer.valueOf(démarrerAligné + taille), Integer.valueOf(tailleFinal));
            }
            régionUtilisé.put(Integer.valueOf(démarrerAligné), Integer.valueOf(taille));
            Arrays.fill(EspaceMémoire, démarrerAligné, démarrerAligné + taille, (byte) 0);
            return démarrerAligné;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void libérerStockage(int adresse) {
        Integer objetTaille = régionUtilisé.remove(Integer.valueOf(adresse));
        if (objetTaille == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int lancer = adresse;
        int taille = objetTaille.intValue();
        Map.Entry<Integer, Integer> valeurAvantCôté = régionVide.lowerEntry(Integer.valueOf(lancer));
        if (valeurAvantCôté != null && valeurAvantCôté.getKey().intValue() + valeurAvantCôté.getValue().intValue() == lancer) {
            lancer = valeurAvantCôté.getKey().intValue();
            taille += valeurAvantCôté.getValue().intValue();
            régionVide.remove(valeurAvantCôté.getKey());
        }
        Map.Entry<Integer, Integer> valeurRetourArrièreCôté = régionVide.ceilingEntry(Integer.valueOf(lancer));
        if (valeurRetourArrièreCôté != null && lancer + taille == valeurRetourArrièreCôté.getKey().intValue()) {
            taille += valeurRetourArrièreCôté.getValue().intValue();
            régionVide.remove(valeurRetourArrièreCôté.getKey());
        }
        régionVide.put(Integer.valueOf(lancer), Integer.valueOf(taille));
    }

    public synchronized byte lireValeurOctet(int adresse) {
        contrôlerPlage(adresse, 1);
        return EspaceMémoire[adresse];
    }

    public synchronized void écrireValeurOctet(int adresse, byte valeur) {
        contrôlerPlage(adresse, 1);
        EspaceMémoire[adresse] = valeur;
    }

    public synchronized int tailleTotal() {
        return EspaceMémoire.length;
    }

    public synchronized int tailleUtilisé() {
        int valeurTotal = 0;
        for (Integer taille : régionUtilisé.values()) {
            valeurTotal += taille.intValue();
        }
        return valeurTotal;
    }

    private void contrôlerPlage(int adresse, int taille) {
        if (adresse < 0 || taille < 0 || adresse > EspaceMémoire.length - taille) {
            throw new IndexOutOfBoundsException("EspaceMémoire 범위를 벗어났습니다.");
        }
    }
}

