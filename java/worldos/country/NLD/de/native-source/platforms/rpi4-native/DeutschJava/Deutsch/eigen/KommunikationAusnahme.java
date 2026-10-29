// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** KommunikationAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class KommunikationAusnahme extends EingabeAusgabeAusnahme {
    public KommunikationAusnahme() { super(); }
    public KommunikationAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
