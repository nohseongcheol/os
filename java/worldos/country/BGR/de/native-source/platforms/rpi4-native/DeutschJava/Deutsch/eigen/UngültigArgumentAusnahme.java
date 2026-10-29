// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** UngültigArgumentAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class UngültigArgumentAusnahme extends java.lang.IllegalArgumentException {
    public UngültigArgumentAusnahme() { super(); }
    public UngültigArgumentAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
