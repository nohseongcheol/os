// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** 한국어로 deklaracja·던지기·잡기를 할 identyfikator 있는 wykonanie_wyjątek. */
public class wykonanie_wyjątek extends java.lang.RuntimeException {
    public wykonanie_wyjątek() { super(); }
    public wykonanie_wyjątek(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
