// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 선언·던지기·잡기를 할 수 있는 TABLO_Store_foo. */
public class TABLO_Store_foo extends java.lang.ArrayStoreException {
    public TABLO_Store_foo() { super(); }
    public TABLO_Store_foo(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
