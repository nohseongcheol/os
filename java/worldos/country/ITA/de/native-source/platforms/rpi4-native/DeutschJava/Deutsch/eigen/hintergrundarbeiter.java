// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Vom Ablaufplaner der eigenen JVM verwalteter Ausführungsstrom, ohne einen Standard-Thread zu umhüllen. */
public final class hintergrundarbeiter {
    public hintergrundarbeiter(AusführbarAufgabe AufgabeAktion) {
        throw new StatuswertAusnahme("Die eigene JVM muss Ausführungsfäden über die deutsche API erstellen können.");
    }
    public native void aufgabeStarten() throws AusführungsfadenStatuswertAusnahme;
    public native void abwarten() throws WartenUnterbrochenAusnahme;
    public native boolean istLebendig();
    public static native void aufgabeAbgeben();
}
