// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** NullverweisVerweisAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class NullverweisVerweisAusnahme extends java.lang.NullPointerException {
    public NullverweisVerweisAusnahme() { super(); }
    public NullverweisVerweisAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
