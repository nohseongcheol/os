// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Liechtenstein.JLieOS.Eingabewert;

import java.util.ArrayDeque;
import java.util.Queue;

/** Übergibt Eingabeereignisse sicher zwischen Interrupts und verwaltetem Code. */
public final class EingabeVerwalter {
    private final Queue<eingabeEreignis> ereignisseListe = new ArrayDeque<eingabeEreignis>();
    private final int höchstwertEreignisAnzahl;
    private int verworfenAnzahlEreignisAnzahl;

    public EingabeVerwalter(int höchstwertEreignisAnzahl) {
        if (höchstwertEreignisAnzahl <= 0) {
            throw new IllegalArgumentException("ereignis 수가 올바르지 않습니다.");
        }
        this.höchstwertEreignisAnzahl = höchstwertEreignisAnzahl;
    }

    public synchronized void tasteAbwärts(int tasteDaten) {
        wertAblegen(new eingabeEreignis(eingabeEreignis.artWert.tasteAbwärts, tasteDaten & 0xff, 0));
    }

    public synchronized void tasteAufwärts(int tasteDaten) {
        wertAblegen(new eingabeEreignis(eingabeEreignis.artWert.tasteAufwärts, tasteDaten & 0xff, 0));
    }

    public synchronized void mausBewegung(int waagerechtPosition, int senkrechtPosition) {
        wertAblegen(new eingabeEreignis(eingabeEreignis.artWert.mausBewegung, waagerechtPosition, senkrechtPosition));
    }

    public synchronized eingabeEreignis nächsterEreignis() {
        return ereignisseListe.poll();
    }

    public synchronized int verworfenAnzahlEreignisAnzahl() {
        return verworfenAnzahlEreignisAnzahl;
    }

    private void wertAblegen(eingabeEreignis ereignis) {
        if (ereignisseListe.size() == höchstwertEreignisAnzahl) {
            ereignisseListe.poll();
            verworfenAnzahlEreignisAnzahl++;
        }
        ereignisseListe.offer(ereignis);
    }
}

