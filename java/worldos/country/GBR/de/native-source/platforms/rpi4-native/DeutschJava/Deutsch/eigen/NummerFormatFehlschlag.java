// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** NummerFormatFehlschlag: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class NummerFormatFehlschlag extends UngültigArgumentAusnahme {
    public NummerFormatFehlschlag() { super(); }
    public NummerFormatFehlschlag(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
