// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;

/** 한국어로 declaración·던지기·잡기를 할 수 있는 숫자형식예외. */
public class 숫자형식예외 extends non_válido_argumento_excepción {
    public 숫자형식예외() { super(); }
    public 숫자형식예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
