// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** 한국어로 declaração·던지기·잡기를 할 número 있는 inválido_argumento_exceção. */
public class inválido_argumento_exceção extends java.lang.IllegalArgumentException {
    public inválido_argumento_exceção() { super(); }
    public inválido_argumento_exceção(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
