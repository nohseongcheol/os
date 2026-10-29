// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** TypTypumwandlungAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class TypTypumwandlungAusnahme extends java.lang.ClassCastException {
    public TypTypumwandlungAusnahme() { super(); }
    public TypTypumwandlungAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
