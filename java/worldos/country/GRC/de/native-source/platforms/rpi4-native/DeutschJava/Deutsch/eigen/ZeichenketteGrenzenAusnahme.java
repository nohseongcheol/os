// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** ZeichenketteGrenzenAusnahme: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class ZeichenketteGrenzenAusnahme extends GrenzenAusnahme {
    public ZeichenketteGrenzenAusnahme() { super(); }
    public ZeichenketteGrenzenAusnahme(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
