// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Übergibt eine Aufgabe an die Ereigniswarteschlange der eigenen Oberfläche. */
public final class EreignisWarteschlange {
    private EreignisWarteschlange() {}
    public static native void späterAufrufen(AusführbarAufgabe AufgabeAktion);
    public static native boolean istEreignisVerteilend();
}
