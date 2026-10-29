// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** WartenZeitüberschreitungAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class WartenZeitüberschreitungAusnahme extends EingabeAusgabeAusnahme {
    public WartenZeitüberschreitungAusnahme() { super(); }
    public WartenZeitüberschreitungAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
