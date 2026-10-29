// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** FehlendDateiAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class FehlendDateiAusnahme extends EingabeAusgabeAusnahme {
    public FehlendDateiAusnahme() { super(); }
    public FehlendDateiAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
