// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** 한국어로 deklarácia·던지기·잡기를 할 수 있는 NEPLATNÝ_zdroj_výnimka. */
public class NEPLATNÝ_zdroj_výnimka extends java.lang.NullPointerException {
    public NEPLATNÝ_zdroj_výnimka() { super(); }
    public NEPLATNÝ_zdroj_výnimka(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
