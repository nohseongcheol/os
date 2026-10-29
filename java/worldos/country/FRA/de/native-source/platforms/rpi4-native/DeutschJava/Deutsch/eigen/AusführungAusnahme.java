// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** AusführungAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class AusführungAusnahme extends java.lang.RuntimeException {
    public AusführungAusnahme() { super(); }
    public AusführungAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
