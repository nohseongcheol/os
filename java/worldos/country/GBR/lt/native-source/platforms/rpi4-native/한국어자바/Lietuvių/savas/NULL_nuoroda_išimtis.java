// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** 한국어로 deklaracija·던지기·잡기를 할 numeris 있는 NULL_nuoroda_išimtis. */
public class NULL_nuoroda_išimtis extends java.lang.NullPointerException {
    public NULL_nuoroda_išimtis() { super(); }
    public NULL_nuoroda_išimtis(String aprašas) { super(aprašas); }
    public String aprašas() { return getMessage(); }
}
