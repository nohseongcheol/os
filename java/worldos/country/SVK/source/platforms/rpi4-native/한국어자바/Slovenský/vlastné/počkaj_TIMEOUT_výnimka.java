// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** 한국어로 deklarácia·던지기·잡기를 할 수 있는 počkaj_TIMEOUT_výnimka. */
public class počkaj_TIMEOUT_výnimka extends vstup_a_výstup_výnimka {
    public počkaj_TIMEOUT_výnimka() { super(); }
    public počkaj_TIMEOUT_výnimka(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
