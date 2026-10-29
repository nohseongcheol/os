// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** 한국어로 declaração·던지기·잡기를 할 número 있는 E_S_exceção. */
public class E_S_exceção extends java.io.IOException {
    public E_S_exceção() { super(); }
    public E_S_exceção(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
