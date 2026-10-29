// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** ausnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class ausnahme extends java.lang.Exception {
    public ausnahme() { super(); }
    public ausnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
