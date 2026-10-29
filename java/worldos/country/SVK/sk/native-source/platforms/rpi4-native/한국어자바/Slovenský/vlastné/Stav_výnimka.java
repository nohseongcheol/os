// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** 한국어로 deklarácia·던지기·잡기를 할 수 있는 Stav_výnimka. */
public class Stav_výnimka extends java.lang.IllegalStateException {
    public Stav_výnimka() { super(); }
    public Stav_výnimka(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
