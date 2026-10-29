// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** 한국어로 deklaracja·던지기·잡기를 할 identyfikator 있는 wątek_Stan_wyjątek. */
public class wątek_Stan_wyjątek extends java.lang.IllegalThreadStateException {
    public wątek_Stan_wyjątek() { super(); }
    public wątek_Stan_wyjątek(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
