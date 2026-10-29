// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kanada.JCanOS.Gerät;

/** Verwaltet PIT-Takte und den Zeitpunkt der Verdrängung. */
public final class Uhr {
    private final int takteJeZweiter;
    private long taktAnzahl;

    public Uhr(int takteJeZweiter) {
        if (takteJeZweiter <= 0) {
            throw new IllegalArgumentException("초당 taktWert 수가 올바르지 않습니다.");
        }
        this.takteJeZweiter = takteJeZweiter;
    }

    public long taktWert() {
        return ++taktAnzahl;
    }

    public long taktAnzahl() {
        return taktAnzahl;
    }

    public long vergangenMillisekunden() {
        return taktAnzahl * 1000L / takteJeZweiter;
    }
}

