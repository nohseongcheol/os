// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** NegativDatenfeldGrößeFehlschlag: Ausnahme, die sich über die deutsche API deklarieren, auslösen und abfangen lässt. */
public class NegativDatenfeldGrößeFehlschlag extends java.lang.NegativeArraySizeException {
    public NegativDatenfeldGrößeFehlschlag() { super(); }
    public NegativDatenfeldGrößeFehlschlag(String beschreibung) { super(beschreibung); }
    public String beschreibung() { return getMessage(); }
}
