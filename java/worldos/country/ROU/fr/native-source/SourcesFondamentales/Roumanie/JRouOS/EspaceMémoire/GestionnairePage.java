// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Roumanie.JRouOS.EspaceMémoire;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** Fournit le mappage de pages de 4 KiB et la copie à l’écriture. */
public final class GestionnairePage {
    public static final int taillePage = 4096;

    private static final class valeurPage {
        private byte[] Données = new byte[taillePage];
        private int nombreÉlémentsRéférence = 1;
        private boolean peutÉcrire = true;
        private boolean copierÉcrireActivé;
    }

    public static final class EspaceAdresse {
        private final Map<Integer, valeurPage> tablePage = new HashMap<Integer, valeurPage>();
    }

    public EspaceAdresse espaceAdresseNouveau() {
        return new EspaceAdresse();
    }

    public void pageTableCorrespondance(EspaceAdresse régionAdresse, int adresseVirtuel, boolean peutÉcrire) {
        int numéro = numéroPage(adresseVirtuel);
        valeurPage pageNouveau = new valeurPage();
        pageNouveau.peutÉcrire = peutÉcrire;
        régionAdresse.tablePage.put(Integer.valueOf(numéro), pageNouveau);
    }

    public EspaceAdresse écrireActivéCopierCloner(EspaceAdresse original) {
        EspaceAdresse valeurCloné = new EspaceAdresse();
        for (Map.Entry<Integer, valeurPage> valeurEntréeÉlément : original.tablePage.entrySet()) {
            valeurPage pagePartagé = valeurEntréeÉlément.getValue();
            pagePartagé.nombreÉlémentsRéférence++;
            if (pagePartagé.peutÉcrire) {
                pagePartagé.peutÉcrire = false;
                pagePartagé.copierÉcrireActivé = true;
            }
            valeurCloné.tablePage.put(valeurEntréeÉlément.getKey(), pagePartagé);
        }
        return valeurCloné;
    }

    public byte lireValeurOctet(EspaceAdresse régionAdresse, int adresseVirtuel) {
        valeurPage valeurCible = trouverPage(régionAdresse, adresseVirtuel);
        return valeurCible.Données[Math.floorMod(adresseVirtuel, taillePage)];
    }

    public void écrireValeurOctet(EspaceAdresse régionAdresse, int adresseVirtuel, byte valeur) {
        int numéro = numéroPage(adresseVirtuel);
        valeurPage valeurCible = trouverPage(régionAdresse, adresseVirtuel);
        if (!valeurCible.peutÉcrire) {
            if (!valeurCible.copierÉcrireActivé) {
                throw new IllegalStateException("lire 전용 쪽입니다.");
            }
            valeurCible = créerPagePrivé(régionAdresse, numéro, valeurCible);
        }
        valeurCible.Données[Math.floorMod(adresseVirtuel, taillePage)] = valeur;
    }

    public void écrirePlagePrivé(EspaceAdresse régionAdresse, int démarrerAdresse, int taille) {
        if (taille < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int adresseFin = Math.addExact(démarrerAdresse, taille);
        for (int adresse = démarrerAdresse; adresse < adresseFin; adresse = (numéroPage(adresse) + 1) * taillePage) {
            int numéro = numéroPage(adresse);
            valeurPage valeurCible = trouverPage(régionAdresse, adresse);
            if (valeurCible.copierÉcrireActivé) {
                créerPagePrivé(régionAdresse, numéro, valeurCible);
            } else {
                valeurCible.peutÉcrire = true;
            }
        }
    }

    public void écrirePlage(EspaceAdresse régionAdresse, int démarrerAdresse, byte[] Données) {
        for (int numéro = 0; numéro < Données.length; numéro++) {
            écrireValeurOctet(régionAdresse, démarrerAdresse + numéro, Données[numéro]);
        }
    }

    private valeurPage créerPagePrivé(EspaceAdresse régionAdresse, int numéro, valeurPage pagePartagé) {
        valeurPage pagePrivé = new valeurPage();
        pagePrivé.Données = Arrays.copyOf(pagePartagé.Données, pagePartagé.Données.length);
        pagePrivé.peutÉcrire = true;
        pagePrivé.copierÉcrireActivé = false;
        pagePartagé.nombreÉlémentsRéférence--;
        régionAdresse.tablePage.put(Integer.valueOf(numéro), pagePrivé);
        return pagePrivé;
    }

    private valeurPage trouverPage(EspaceAdresse régionAdresse, int adresse) {
        valeurPage valeurCible = régionAdresse.tablePage.get(Integer.valueOf(numéroPage(adresse)));
        if (valeurCible == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return valeurCible;
    }

    private int numéroPage(int adresse) {
        if (adresse < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return adresse / taillePage;
    }
}

