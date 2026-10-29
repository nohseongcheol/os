// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** 한국어로 declaração·던지기·잡기를 할 número 있는 Estado_exceção. */
public class Estado_exceção extends java.lang.IllegalStateException {
    public Estado_exceção() { super(); }
    public Estado_exceção(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
