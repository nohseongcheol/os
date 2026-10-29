// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** 한국어로 declaração·던지기·잡기를 할 número 있는 comunicação_exceção. */
public class comunicação_exceção extends E_S_exceção {
    public comunicação_exceção() { super(); }
    public comunicação_exceção(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
