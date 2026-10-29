// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** AusführungsfadenStatuswertAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class AusführungsfadenStatuswertAusnahme extends java.lang.IllegalThreadStateException {
    public AusführungsfadenStatuswertAusnahme() { super(); }
    public AusführungsfadenStatuswertAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
