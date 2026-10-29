// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Ein Ausführungsfaden ist ein Ausführungsstrom. Die eigene JVM wechselt nach der Zahl ausgeführter Anweisungen zwischen den Fäden. */
public final class Aufgabe {
    private Aufgabe() {}
    public static hintergrundarbeiter ausführenVorgang(AusführbarAufgabe AufgabeAktion) { hintergrundarbeiter ausführungsfadenWert = new hintergrundarbeiter(AufgabeAktion); ausführungsfadenWert.aufgabeStarten(); return ausführungsfadenWert; }
    public static void abwarten(hintergrundarbeiter ausführungsfadenWert) throws WartenUnterbrochenAusnahme { ausführungsfadenWert.abwarten(); }
    public static boolean istLebendig(hintergrundarbeiter ausführungsfadenWert) { return ausführungsfadenWert.istLebendig(); }
    public static void aufgabeAbgeben() { hintergrundarbeiter.aufgabeAbgeben(); }
}
