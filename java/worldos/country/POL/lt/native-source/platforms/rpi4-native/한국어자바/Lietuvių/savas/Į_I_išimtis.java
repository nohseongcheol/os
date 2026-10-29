// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** 한국어로 deklaracija·던지기·잡기를 할 numeris 있는 Į_I_išimtis. */
public class Į_I_išimtis extends java.io.IOException {
    public Į_I_išimtis() { super(); }
    public Į_I_išimtis(String aprašas) { super(aprašas); }
    public String aprašas() { return getMessage(); }
}
