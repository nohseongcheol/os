// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** Zeigt den Abbruch eines auf einen Ausführungsfaden wartenden Vorgangs an, nicht die Beendigung der Aufgabe selbst. */
public class WartenUnterbrochenAusnahme extends java.lang.InterruptedException {
    public WartenUnterbrochenAusnahme() { super(); }
    public WartenUnterbrochenAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
