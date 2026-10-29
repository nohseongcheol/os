// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** 한국어로 declaração·던지기·잡기를 할 número 있는 referência_nula_exceção. */
public class referência_nula_exceção extends java.lang.NullPointerException {
    public referência_nula_exceção() { super(); }
    public referência_nula_exceção(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
