// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** StatuswertAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class StatuswertAusnahme extends java.lang.IllegalStateException {
    public StatuswertAusnahme() { super(); }
    public StatuswertAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
