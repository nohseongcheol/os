// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mali.JMliOS.périphériqueStockage;

import java.util.Arrays;

/** Périphérique à secteurs logiques de 512 octets correspondant à la couche de commandes ATA 28 bits. */
public final class PièceJointeTechnologieAvancé {
    public static final int tailleSection = 512;
    private final byte[] Données;
    private final boolean lireValeurSeulement;

    public PièceJointeTechnologieAvancé(int nombreÉlémentsSection, boolean lireValeurSeulement) {
        if (nombreÉlémentsSection <= 0) {
            throw new IllegalArgumentException("valeurSection 수가 올바르지 않습니다.");
        }
        Données = new byte[Math.multiplyExact(nombreÉlémentsSection, tailleSection)];
        this.lireValeurSeulement = lireValeurSeulement;
    }

    public int nombreÉlémentsSection() {
        return Données.length / tailleSection;
    }

    public void lire(int indiceSection, byte[] recevoirDestination) {
        contrôlerPlage(indiceSection, recevoirDestination);
        System.arraycopy(Données, indiceSection * tailleSection, recevoirDestination, 0, tailleSection);
    }

    public void écrire(int indiceSection, byte[] écrireVersDonnées) {
        if (lireValeurSeulement) {
            throw new IllegalStateException("lire 전용 장치입니다.");
        }
        contrôlerPlage(indiceSection, écrireVersDonnées);
        System.arraycopy(écrireVersDonnées, 0, Données, indiceSection * tailleSection, tailleSection);
    }

    public void effacerEntréeÉlément() {
        if (lireValeurSeulement) {
            throw new IllegalStateException("lire 전용 장치입니다.");
        }
        Arrays.fill(Données, (byte) 0);
    }

    private void contrôlerPlage(int indiceSection, byte[] espaceTemporaire) {
        if (indiceSection < 0 || indiceSection >= nombreÉlémentsSection() || espaceTemporaire.length < tailleSection) {
            throw new IllegalArgumentException("ATA valeurSection 범위가 올바르지 않습니다.");
        }
    }
}

