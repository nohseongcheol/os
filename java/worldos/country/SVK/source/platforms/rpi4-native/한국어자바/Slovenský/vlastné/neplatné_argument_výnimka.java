// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovenský.vlastné;

/** 한국어로 deklarácia·던지기·잡기를 할 수 있는 neplatné_argument_výnimka. */
public class neplatné_argument_výnimka extends java.lang.IllegalArgumentException {
    public neplatné_argument_výnimka() { super(); }
    public neplatné_argument_výnimka(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
