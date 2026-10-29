// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Irlande.JIrlOS.entréeÉlémentDescripteur;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Conserve les réglages de la table globale des descripteurs x86 et du segment d’état de tâche. */
public final class TableDescripteurGlobal {
    public static final class valeurFragment {
        private final int valeurArrièrePlan;
        private final int limiteFrontière;
        private final int valeurAccès;

        valeurFragment(int valeurArrièrePlan, int limiteFrontière, int valeurAccès) {
            this.valeurArrièrePlan = valeurArrièrePlan;
            this.limiteFrontière = limiteFrontière;
            this.valeurAccès = valeurAccès;
        }

        public int valeurArrièrePlan() { return valeurArrièrePlan; }
        public int limiteFrontière() { return limiteFrontière; }
        public int valeurAccès() { return valeurAccès; }
    }

    private final List<valeurFragment> listeFragments = new ArrayList<valeurFragment>();

    public int ajouterFinEntréeÉlément(int valeurArrièrePlan, int limiteFrontière, int valeurAccès) {
        listeFragments.add(new valeurFragment(valeurArrièrePlan, limiteFrontière, valeurAccès));
        return (listeFragments.size() - 1) * 8;
    }

    public List<valeurFragment> listeFragments() {
        return Collections.unmodifiableList(listeFragments);
    }

    public void définirValeurDéfaut() {
        listeFragments.clear();
        ajouterFinEntréeÉlément(0, 0, 0);
        ajouterFinEntréeÉlément(0, 0xfffff, 0x9a);
        ajouterFinEntréeÉlément(0, 0xfffff, 0x92);
        ajouterFinEntréeÉlément(0, 0xfffff, 0xfa);
        ajouterFinEntréeÉlément(0, 0xfffff, 0xf2);
    }
}

