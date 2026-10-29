// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** DatenfeldAblegenDatenFehlschlag: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class DatenfeldAblegenDatenFehlschlag extends java.lang.ArrayStoreException {
    public DatenfeldAblegenDatenFehlschlag() { super(); }
    public DatenfeldAblegenDatenFehlschlag(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
