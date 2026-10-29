// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** 한국어로 deklaracja·던지기·잡기를 할 identyfikator 있는 komunikacja_wyjątek. */
public class komunikacja_wyjątek extends We_Wy_wyjątek {
    public komunikacja_wyjątek() { super(); }
    public komunikacja_wyjątek(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
