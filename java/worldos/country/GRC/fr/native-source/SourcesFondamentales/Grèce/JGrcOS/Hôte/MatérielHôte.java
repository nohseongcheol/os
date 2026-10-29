// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Grèce.JGrcOS.Hôte;

import java.util.HashMap;
import java.util.Map;
import Grèce.JGrcOS.Noyau.valeurMatériel;

/** Substitut matériel pour tester de façon déterministe le noyau géré sur une JVM ordinaire. */
public final class MatérielHôte implements valeurMatériel {
    private final Map<Integer, Integer> valeurPortMatériel = new HashMap<Integer, Integer>();
    private final StringBuilder journalSériel = new StringBuilder();

    @Override
    public void sortieSériel(String valeurContenuValeur) {
        journalSériel.append(valeurContenuValeur);
        System.out.print(valeurContenuValeur);
    }

    @Override
    public int lireOctetPort(int numéroPortMatériel) {
        Integer valeur = valeurPortMatériel.get(Integer.valueOf(numéroPortMatériel));
        return valeur == null ? 0 : valeur.intValue();
    }

    @Override
    public void écrireOctetPort(int numéroPortMatériel, int valeur) {
        valeurPortMatériel.put(Integer.valueOf(numéroPortMatériel), Integer.valueOf(valeur & 0xff));
    }

    @Override
    public void cPUArrêterMachine() {
        // Pendant les tests hôtes, revenir immédiatement sans attendre l’événement suivant.
    }

    public String journalSériel() {
        return journalSériel.toString();
    }
}

