// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Frankreich.JFraOS.speichergerätGerät;

import java.util.Arrays;

/** Gerät mit logischen 512-Byte-Sektoren entsprechend der ATA-28-Bit-Befehlsschicht. */
public final class FortgeschrittenTechnikAnhang {
    public static final int abschnittGröße = 512;
    private final byte[] Daten;
    private final boolean ausschließlichWertLesen;

    public FortgeschrittenTechnikAnhang(int abschnittAnzahl, boolean ausschließlichWertLesen) {
        if (abschnittAnzahl <= 0) {
            throw new IllegalArgumentException("abschnittWert 수가 올바르지 않습니다.");
        }
        Daten = new byte[Math.multiplyExact(abschnittAnzahl, abschnittGröße)];
        this.ausschließlichWertLesen = ausschließlichWertLesen;
    }

    public int abschnittAnzahl() {
        return Daten.length / abschnittGröße;
    }

    public void lesen(int abschnittIndex, byte[] zielEmpfangen) {
        bereichPrüfen(abschnittIndex, zielEmpfangen);
        System.arraycopy(Daten, abschnittIndex * abschnittGröße, zielEmpfangen, 0, abschnittGröße);
    }

    public void schreiben(int abschnittIndex, byte[] datenNachSchreiben) {
        if (ausschließlichWertLesen) {
            throw new IllegalStateException("lesen 전용 장치입니다.");
        }
        bereichPrüfen(abschnittIndex, datenNachSchreiben);
        System.arraycopy(datenNachSchreiben, 0, Daten, abschnittIndex * abschnittGröße, abschnittGröße);
    }

    public void eintragTilgen() {
        if (ausschließlichWertLesen) {
            throw new IllegalStateException("lesen 전용 장치입니다.");
        }
        Arrays.fill(Daten, (byte) 0);
    }

    private void bereichPrüfen(int abschnittIndex, byte[] vorläufigRaum) {
        if (abschnittIndex < 0 || abschnittIndex >= abschnittAnzahl() || vorläufigRaum.length < abschnittGröße) {
            throw new IllegalArgumentException("ATA abschnittWert 범위가 올바르지 않습니다.");
        }
    }
}

