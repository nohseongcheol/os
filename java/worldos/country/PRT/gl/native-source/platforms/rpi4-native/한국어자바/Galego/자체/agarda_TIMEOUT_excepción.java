// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;

/** 한국어로 declaración·던지기·잡기를 할 수 있는 agarda_TIMEOUT_excepción. */
public class agarda_TIMEOUT_excepción extends E_S_excepción {
    public agarda_TIMEOUT_excepción() { super(); }
    public agarda_TIMEOUT_excepción(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
