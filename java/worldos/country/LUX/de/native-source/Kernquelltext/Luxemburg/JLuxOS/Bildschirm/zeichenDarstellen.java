// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Luxemburg.JLuxOS.Bildschirm;

import java.util.Arrays;

/** Modell einer Zeichenanzeige mit 80x25 Zeichen wie im VGA-Textmodus. */
public final class zeichenDarstellen {
    public static final int breiteWert = 80;
    public static final int höheWert = 25;
    private final char[] zeichenWerte = new char[breiteWert * höheWert];
    private int waagerechtPosition;
    private int senkrechtPosition;

    public zeichenDarstellen() {
        eintragTilgen();
    }

    public void Ausgabe(String inhaltswertWert) {
        for (int Nummer = 0; Nummer < inhaltswertWert.length(); Nummer++) {
            char Zeichen = inhaltswertWert.charAt(Nummer);
            if (Zeichen == '\n') {
                waagerechtPosition = 0;
                senkrechtPosition++;
            } else {
                zeichenDrucken(waagerechtPosition++, senkrechtPosition, Zeichen);
            }
            if (waagerechtPosition >= breiteWert) {
                waagerechtPosition = 0;
                senkrechtPosition++;
            }
            if (senkrechtPosition >= höheWert) {
                rollenAufwärts();
            }
        }
    }

    public char Zeichen(int waagerechtPosition, int senkrechtPosition) {
        positionÜberprüfen(waagerechtPosition, senkrechtPosition);
        return zeichenWerte[senkrechtPosition * breiteWert + waagerechtPosition];
    }

    public void eintragTilgen() {
        Arrays.fill(zeichenWerte, ' ');
        waagerechtPosition = 0;
        senkrechtPosition = 0;
    }

    private void zeichenDrucken(int waagerechtPosition, int senkrechtPosition, char Zeichen) {
        positionÜberprüfen(waagerechtPosition, senkrechtPosition);
        zeichenWerte[senkrechtPosition * breiteWert + waagerechtPosition] = Zeichen;
    }

    private void rollenAufwärts() {
        System.arraycopy(zeichenWerte, breiteWert, zeichenWerte, 0, breiteWert * (höheWert - 1));
        Arrays.fill(zeichenWerte, breiteWert * (höheWert - 1), zeichenWerte.length, ' ');
        senkrechtPosition = höheWert - 1;
    }

    private void positionÜberprüfen(int waagerechtPosition, int senkrechtPosition) {
        if (waagerechtPosition < 0 || waagerechtPosition >= breiteWert || senkrechtPosition < 0 || senkrechtPosition >= höheWert) {
            throw new IllegalArgumentException("Bildschirm 위치가 올바르지 않습니다.");
        }
    }
}

