// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Hilfsmethoden zum Erzeugen von Anzeigekomponenten der deutschen API. */
public final class Bedienelement {
    private Bedienelement() {}
    public static void späterAufrufen(AusführbarAufgabe AufgabeAktion) { EreignisWarteschlange.späterAufrufen(AufgabeAktion); }
    public static beschriftung kennzeichenWert(String Text, int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int höheWert) {
        return new beschriftung(Text, waagerechtPosition, senkrechtPosition, breiteSpannweite, höheWert);
    }
    public static schaltfläche schaltfläche(String Text, int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int höheWert, AktionEmpfänger empfängerWert) {
        return new schaltfläche(Text, waagerechtPosition, senkrechtPosition, breiteSpannweite, höheWert, empfängerWert);
    }
    public static TextFeld TextFeld(String Text, int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int höheWert) {
        return new TextFeld(Text, waagerechtPosition, senkrechtPosition, breiteSpannweite, höheWert);
    }
}
