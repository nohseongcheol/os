// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** 한국어로 deklarácia·던지기·잡기를 할 수 있는 vlákno_Stav_výnimka. */
public class vlákno_Stav_výnimka extends java.lang.IllegalThreadStateException {
    public vlákno_Stav_výnimka() { super(); }
    public vlákno_Stav_výnimka(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
