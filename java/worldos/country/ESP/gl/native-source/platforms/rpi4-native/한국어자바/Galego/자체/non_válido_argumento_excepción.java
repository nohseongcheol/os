// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;

/** 한국어로 declaración·던지기·잡기를 할 수 있는 non_válido_argumento_excepción. */
public class non_válido_argumento_excepción extends java.lang.IllegalArgumentException {
    public non_válido_argumento_excepción() { super(); }
    public non_válido_argumento_excepción(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
