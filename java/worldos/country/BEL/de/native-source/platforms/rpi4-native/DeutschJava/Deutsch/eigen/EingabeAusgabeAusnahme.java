// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** EingabeAusgabeAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class EingabeAusgabeAusnahme extends java.io.IOException {
    public EingabeAusgabeAusnahme() { super(); }
    public EingabeAusgabeAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
