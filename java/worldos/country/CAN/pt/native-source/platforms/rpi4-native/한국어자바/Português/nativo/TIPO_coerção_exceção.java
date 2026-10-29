// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** 한국어로 declaração·던지기·잡기를 할 número 있는 TIPO_coerção_exceção. */
public class TIPO_coerção_exceção extends java.lang.ClassCastException {
    public TIPO_coerção_exceção() { super(); }
    public TIPO_coerção_exceção(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
