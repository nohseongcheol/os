// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Català.propi;

/** 한국어로 declaració·던지기·잡기를 할 수 있는 MATRIU_Store_error. */
public class MATRIU_Store_error extends java.lang.ArrayStoreException {
    public MATRIU_Store_error() { super(); }
    public MATRIU_Store_error(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
