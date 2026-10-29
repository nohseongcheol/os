// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Direkt mit der eigenen JVM und der Fensterverwaltung des Kernels verbundenes Fenster. */
public final class fenster extends BildschirmElement {
    public fenster(String fensterTitel, int breiteSpannweite, int höheWert) {
        throw new StatuswertAusnahme("Die eigene JVM muss Fenster über die deutsche API erstellen können.");
    }
    public native void elementHinzufügen(BildschirmElement elementWert);
    public native void fensterAnzeigen();
    public native void schließen();
    public native boolean istSichtbar();
}
