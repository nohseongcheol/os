// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** AdresseNachschlagenAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class AdresseNachschlagenAusnahme extends EingabeAusgabeAusnahme {
    public AdresseNachschlagenAusnahme() { super(); }
    public AdresseNachschlagenAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
