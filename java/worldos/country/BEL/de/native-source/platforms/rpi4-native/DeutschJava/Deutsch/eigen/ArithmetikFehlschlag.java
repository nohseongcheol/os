// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** ArithmetikFehlschlag: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class ArithmetikFehlschlag extends java.lang.ArithmeticException {
    public ArithmetikFehlschlag() { super(); }
    public ArithmetikFehlschlag(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
