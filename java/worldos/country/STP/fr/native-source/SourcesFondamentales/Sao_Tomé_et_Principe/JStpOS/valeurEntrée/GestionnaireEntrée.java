// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sao_Tomé_et_Principe.JStpOS.valeurEntrée;

import java.util.ArrayDeque;
import java.util.Queue;

/** Transmet les événements d’entrée en sûreté entre interruptions et code géré. */
public final class GestionnaireEntrée {
    private final Queue<évènementEntrée> listeÉvènements = new ArrayDeque<évènementEntrée>();
    private final int nombreÉlémentsÉvènementMaximal;
    private int nombreÉlémentsÉvènementAbandonnésNombre;

    public GestionnaireEntrée(int nombreÉlémentsÉvènementMaximal) {
        if (nombreÉlémentsÉvènementMaximal <= 0) {
            throw new IllegalArgumentException("évènement 수가 올바르지 않습니다.");
        }
        this.nombreÉlémentsÉvènementMaximal = nombreÉlémentsÉvènementMaximal;
    }

    public synchronized void basDirectionTouche(int donnéesTouche) {
        placerValeur(new évènementEntrée(évènementEntrée.valeurGenre.basDirectionTouche, donnéesTouche & 0xff, 0));
    }

    public synchronized void hautDirectionTouche(int donnéesTouche) {
        placerValeur(new évènementEntrée(évènementEntrée.valeurGenre.hautDirectionTouche, donnéesTouche & 0xff, 0));
    }

    public synchronized void mouvementSouris(int positionHorizontal, int positionVertical) {
        placerValeur(new évènementEntrée(évènementEntrée.valeurGenre.mouvementSouris, positionHorizontal, positionVertical));
    }

    public synchronized évènementEntrée évènementSuivant() {
        return listeÉvènements.poll();
    }

    public synchronized int nombreÉlémentsÉvènementAbandonnésNombre() {
        return nombreÉlémentsÉvènementAbandonnésNombre;
    }

    private void placerValeur(évènementEntrée évènement) {
        if (listeÉvènements.size() == nombreÉlémentsÉvènementMaximal) {
            listeÉvènements.poll();
            nombreÉlémentsÉvènementAbandonnésNombre++;
        }
        listeÉvènements.offer(évènement);
    }
}

