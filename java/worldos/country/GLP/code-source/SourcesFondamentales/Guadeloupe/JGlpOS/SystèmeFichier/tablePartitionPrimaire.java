// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Guadeloupe.JGlpOS.SystèmeFichier;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Lit les quatre partitions primaires d’un MBR DOS. */
public final class tablePartitionPrimaire {
    public static final class valeurPartition {
        private final int valeurGenre;
        private final long démarrerSection;
        private final long nombreÉlémentsSection;

        valeurPartition(int valeurGenre, long démarrerSection, long nombreÉlémentsSection) {
            this.valeurGenre = valeurGenre;
            this.démarrerSection = démarrerSection;
            this.nombreÉlémentsSection = nombreÉlémentsSection;
        }

        public int valeurGenre() { return valeurGenre; }
        public long démarrerSection() { return démarrerSection; }
        public long nombreÉlémentsSection() { return nombreÉlémentsSection; }
    }

    public List<valeurPartition> lire(byte[] sectionPremier) {
        if (sectionPremier == null || sectionPremier.length < 512
                || (sectionPremier[510] & 0xff) != 0x55 || (sectionPremier[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<valeurPartition> résultat = new ArrayList<valeurPartition>();
        for (int numéro = 0; numéro < 4; numéro++) {
            int position = 446 + numéro * 16;
            int valeurGenre = sectionPremier[position + 4] & 0xff;
            long lancer = entierOrdreOctetsPetit(sectionPremier, position + 8);
            long taille = entierOrdreOctetsPetit(sectionPremier, position + 12);
            if (valeurGenre != 0 && taille != 0) {
                résultat.add(new valeurPartition(valeurGenre, lancer, taille));
            }
        }
        return Collections.unmodifiableList(résultat);
    }

    private long entierOrdreOctetsPetit(byte[] Données, int position) {
        return (Données[position] & 0xffL)
                | ((Données[position + 1] & 0xffL) << 8)
                | ((Données[position + 2] & 0xffL) << 16)
                | ((Données[position + 3] & 0xffL) << 24);
    }
}

