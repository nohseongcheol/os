// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Litauen.JLtuOS.Aufgabe;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Litauen.JLtuOS.Speicherraum.SeiteVerwalter;
import Litauen.JLtuOS.DateiSystem.dateiDeskriptorTabelle;

/** Verwaltet Prozesskennungen und eine umlaufende Bereitschaftswarteschlange. */
public final class Ablaufplaner {
    private final SeiteVerwalter seiteVerwaltung;
    private final Map<Integer, prozessWert> prozessListe = new HashMap<Integer, prozessWert>();
    private final Queue<prozessWert> bereitWarteschlange = new ArrayDeque<prozessWert>();
    private int nächsterBezeichner = 1;

    public Ablaufplaner(SeiteVerwalter seiteVerwaltung) {
        this.seiteVerwaltung = seiteVerwaltung;
    }

    public prozessWert ersterProzess(dateiDeskriptorTabelle dateiDeskriptor) {
        prozessWert neuProzess = new prozessWert(bezeichnerZuteilen(), 0, seiteVerwaltung.neuAdresseRaum(), dateiDeskriptor);
        prozessListe.put(Integer.valueOf(neuProzess.bezeichnerWert()), neuProzess);
        bereitWarteschlange.offer(neuProzess);
        return neuProzess;
    }

    public prozessWert klonenWert(prozessWert elternknotenWert) {
        prozessWert kindWert = new prozessWert(
                bezeichnerZuteilen(),
                elternknotenWert.bezeichnerWert(),
                seiteVerwaltung.klonenKopierenEingeschaltetSchreiben(elternknotenWert.AdresseRaum()),
                elternknotenWert.dateiDeskriptor().klonenWert());
        kindWert.programmAbbrechenSetzen(elternknotenWert.programmAbbrechen());
        prozessListe.put(Integer.valueOf(kindWert.bezeichnerWert()), kindWert);
        bereitWarteschlange.offer(kindWert);
        return kindWert;
    }

    public prozessWert nächsterProzess() {
        int anzahlPrüfen = bereitWarteschlange.size();
        for (int Nummer = 0; Nummer < anzahlPrüfen; Nummer++) {
            prozessWert nächsterElementeintrag = bereitWarteschlange.poll();
            if (nächsterElementeintrag != null && (nächsterElementeintrag.statuswertWert() == prozessStatuswert.vorbereiten || nächsterElementeintrag.statuswertWert() == prozessStatuswert.befehlAusführen)) {
                nächsterElementeintrag.statuswertSetzen(prozessStatuswert.befehlAusführen);
                bereitWarteschlange.offer(nächsterElementeintrag);
                return nächsterElementeintrag;
            }
        }
        return null;
    }

    public int fürKindWarten(prozessWert elternknotenWert, int kindBezeichner, boolean nichtBlockierend) {
        for (prozessWert kandidat : prozessListe.values()) {
            if (kandidat.elternknotenBezeichner() != elternknotenWert.bezeichnerWert()) {
                continue;
            }
            if (kindBezeichner > 0 && kandidat.bezeichnerWert() != kindBezeichner) {
                continue;
            }
            if (kandidat.statuswertWert() == prozessStatuswert.verlassenProzessProgramm) {
                int ergebnis = (kandidat.verlassenProzessKode() & 0xff) << 8;
                prozessListe.remove(Integer.valueOf(kandidat.bezeichnerWert()));
                return ergebnis;
            }
            return nichtBlockierend ? 0 : -11;
        }
        return -10;
    }

    public prozessWert prozessFinden(int bezeichnerWert) {
        return prozessListe.get(Integer.valueOf(bezeichnerWert));
    }

    private int bezeichnerZuteilen() {
        return nächsterBezeichner++;
    }
}
