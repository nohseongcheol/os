// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Togo.JTgoOS.SystèmeFichier;

import java.util.HashMap;
import java.util.Map;

/** Conserve des descripteurs propres à chaque processus et des descriptions de fichiers ouverts partageables. */
public final class tableDescripteurFichier {
    private static final int descripteurMaximal = 32;

    private static final class entréeÉlémentDescripteur {
        private final SystèmeFichier.fichierOuvert fichierOuvert;
        private boolean fermerOpérationExécutionActivé;

        entréeÉlémentDescripteur(SystèmeFichier.fichierOuvert fichierOuvert) {
            this.fichierOuvert = fichierOuvert;
        }
    }

    private final SystèmeFichier SystèmeFichier;
    private final Map<Integer, entréeÉlémentDescripteur> entréesListeDescripteur = new HashMap<Integer, entréeÉlémentDescripteur>();

    public tableDescripteurFichier(SystèmeFichier SystèmeFichier) {
        this.SystèmeFichier = SystèmeFichier;
    }

    public int ouvrir(String nom) {
        SystèmeFichier.fichierOuvert fichierOuvert = SystèmeFichier.ouvrir(nom);
        if (fichierOuvert == null) {
            return -2;
        }
        int numéro = indiceVide(3);
        if (numéro < 0) {
            return -24;
        }
        entréesListeDescripteur.put(Integer.valueOf(numéro), new entréeÉlémentDescripteur(fichierOuvert));
        return numéro;
    }

    public int lire(int numéro, byte[] recevoirDestination, int taille) {
        entréeÉlémentDescripteur valeurEntréeÉlément = entréesListeDescripteur.get(Integer.valueOf(numéro));
        if (valeurEntréeÉlément == null) {
            return -9;
        }
        if (taille < 0 || taille > recevoirDestination.length) {
            return -22;
        }
        int donnéesResteDivision = valeurEntréeÉlément.fichierOuvert.Données.length - valeurEntréeÉlément.fichierOuvert.position;
        int lireTaille = Math.min(taille, Math.max(donnéesResteDivision, 0));
        System.arraycopy(valeurEntréeÉlément.fichierOuvert.Données, valeurEntréeÉlément.fichierOuvert.position, recevoirDestination, 0, lireTaille);
        valeurEntréeÉlément.fichierOuvert.position += lireTaille;
        return lireTaille;
    }

    public int positionDéplacer(int numéro, int valeurDistance, int racineProjet) {
        entréeÉlémentDescripteur valeurEntréeÉlément = entréesListeDescripteur.get(Integer.valueOf(numéro));
        if (valeurEntréeÉlément == null) {
            return -9;
        }
        int valeurArrièrePlan;
        if (racineProjet == 0) {
            valeurArrièrePlan = 0;
        } else if (racineProjet == 1) {
            valeurArrièrePlan = valeurEntréeÉlément.fichierOuvert.position;
        } else if (racineProjet == 2) {
            valeurArrièrePlan = valeurEntréeÉlément.fichierOuvert.Données.length;
        } else {
            return -22;
        }
        int positionNouveau = valeurArrièrePlan + valeurDistance;
        if (positionNouveau < 0) {
            return -22;
        }
        valeurEntréeÉlément.fichierOuvert.position = positionNouveau;
        return positionNouveau;
    }

    public int fermer(int numéro) {
        entréeÉlémentDescripteur valeurEntréeÉlément = entréesListeDescripteur.remove(Integer.valueOf(numéro));
        if (valeurEntréeÉlément == null) {
            return -9;
        }
        valeurEntréeÉlément.fichierOuvert.nombreÉlémentsRéférence--;
        return 0;
    }

    public int descripteurCloné(int numéro, int numéroMinimal) {
        entréeÉlémentDescripteur valeurEntréeÉlément = entréesListeDescripteur.get(Integer.valueOf(numéro));
        if (valeurEntréeÉlément == null) {
            return -9;
        }
        int numéroNouveau = indiceVide(numéroMinimal);
        if (numéroNouveau < 0) {
            return -24;
        }
        valeurEntréeÉlément.fichierOuvert.nombreÉlémentsRéférence++;
        entréesListeDescripteur.put(Integer.valueOf(numéroNouveau), new entréeÉlémentDescripteur(valeurEntréeÉlément.fichierOuvert));
        return numéroNouveau;
    }

    public int àPositionDuplicata(int numéro, int numéroNouveau) {
        if (numéro == numéroNouveau) {
            return entréesListeDescripteur.containsKey(Integer.valueOf(numéro)) ? numéro : -9;
        }
        if (numéroNouveau < 0 || numéroNouveau >= descripteurMaximal) {
            return -9;
        }
        entréeÉlémentDescripteur original = entréesListeDescripteur.get(Integer.valueOf(numéro));
        if (original == null) {
            return -9;
        }
        if (entréesListeDescripteur.containsKey(Integer.valueOf(numéroNouveau))) {
            fermer(numéroNouveau);
        }
        original.fichierOuvert.nombreÉlémentsRéférence++;
        entréesListeDescripteur.put(Integer.valueOf(numéroNouveau), new entréeÉlémentDescripteur(original.fichierOuvert));
        return numéroNouveau;
    }

    public int définirOpérationExécutionActivéFermer(int numéro, boolean valeur) {
        entréeÉlémentDescripteur valeurEntréeÉlément = entréesListeDescripteur.get(Integer.valueOf(numéro));
        if (valeurEntréeÉlément == null) {
            return -9;
        }
        valeurEntréeÉlément.fermerOpérationExécutionActivé = valeur;
        return 0;
    }

    public int fermerValeurOpérationExécutionActivé(int numéro) {
        entréeÉlémentDescripteur valeurEntréeÉlément = entréesListeDescripteur.get(Integer.valueOf(numéro));
        if (valeurEntréeÉlément == null) {
            return -9;
        }
        return valeurEntréeÉlément.fermerOpérationExécutionActivé ? 1 : 0;
    }

    public informationFichier informationSystème(int numéro) {
        if (numéro >= 0 && numéro <= 2) {
            return new informationFichier(0, 0020666);
        }
        entréeÉlémentDescripteur valeurEntréeÉlément = entréesListeDescripteur.get(Integer.valueOf(numéro));
        if (valeurEntréeÉlément == null) {
            return null;
        }
        return new informationFichier(valeurEntréeÉlément.fichierOuvert.Données.length, 0100444);
    }

    public void fermerOpérationExécutionActivé() {
        Integer[] listeNuméro = entréesListeDescripteur.keySet().toArray(new Integer[0]);
        for (Integer numéro : listeNuméro) {
            entréeÉlémentDescripteur valeurEntréeÉlément = entréesListeDescripteur.get(numéro);
            if (valeurEntréeÉlément != null && valeurEntréeÉlément.fermerOpérationExécutionActivé) {
                fermer(numéro.intValue());
            }
        }
    }

    public boolean estOuvrir(int numéro) {
        return entréesListeDescripteur.containsKey(Integer.valueOf(numéro));
    }

    public tableDescripteurFichier valeurCloner() {
        tableDescripteurFichier résultat = new tableDescripteurFichier(SystèmeFichier);
        for (Map.Entry<Integer, entréeÉlémentDescripteur> valeurEntréeÉlément : entréesListeDescripteur.entrySet()) {
            valeurEntréeÉlément.getValue().fichierOuvert.nombreÉlémentsRéférence++;
            entréeÉlémentDescripteur descripteurNouveau = new entréeÉlémentDescripteur(valeurEntréeÉlément.getValue().fichierOuvert);
            descripteurNouveau.fermerOpérationExécutionActivé = valeurEntréeÉlément.getValue().fermerOpérationExécutionActivé;
            résultat.entréesListeDescripteur.put(valeurEntréeÉlément.getKey(), descripteurNouveau);
        }
        return résultat;
    }

    private int indiceVide(int numéroMinimal) {
        for (int numéro = Math.max(0, numéroMinimal); numéro < descripteurMaximal; numéro++) {
            if (!entréesListeDescripteur.containsKey(Integer.valueOf(numéro))) {
                return numéro;
            }
        }
        return -1;
    }
}
