// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** DatenfeldGrenzenAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class DatenfeldGrenzenAusnahme extends GrenzenAusnahme {
    public DatenfeldGrenzenAusnahme() { super(); }
    public DatenfeldGrenzenAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
