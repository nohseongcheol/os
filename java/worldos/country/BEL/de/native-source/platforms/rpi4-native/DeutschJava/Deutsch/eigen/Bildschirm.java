// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** RGB32-Bildspeicher des eigenständigen Kernels in der beim Start gewählten Größe. */
public final class Bildschirm {
    private Bildschirm() {}
    public static int breiteWert() { int Wert = betriebskernWert.bildschirmBreite(); if (Wert < 0) throw new StatuswertAusnahme("Kein Bildspeicher"); return Wert; }
    public static int höheWert() { int Wert = betriebskernWert.bildschirmHöhe(); if (Wert < 0) throw new StatuswertAusnahme("Kein Bildspeicher"); return Wert; }
    public static void rechteck(int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int höheWert, int farbeWert) {
        if (waagerechtPosition < 0 || senkrechtPosition < 0 || breiteSpannweite < 0 || höheWert < 0 || waagerechtPosition > breiteWert() || senkrechtPosition > höheWert() || breiteSpannweite > breiteWert() - waagerechtPosition || höheWert > höheWert() - senkrechtPosition) throw new UngültigArgumentAusnahme("Bildschirmgrenzen");
        if (betriebskernWert.rechteck(waagerechtPosition, senkrechtPosition, breiteSpannweite, höheWert, farbeWert) < 0) throw new StatuswertAusnahme("Kein Bildspeicher");
    }
    public static void eintragTilgen(int farbeWert) { rechteck(0, 0, breiteWert(), höheWert(), farbeWert); }
    public static void abwarten() { if (betriebskernWert.fürAbbildWarten() < 0) throw new StatuswertAusnahme("Interaktive Eingabe erforderlich"); }
}
