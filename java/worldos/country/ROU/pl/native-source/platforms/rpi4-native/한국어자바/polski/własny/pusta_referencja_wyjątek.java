// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package polski.własny;

/** 한국어로 deklaracja·던지기·잡기를 할 identyfikator 있는 pusta_referencja_wyjątek. */
public class pusta_referencja_wyjątek extends java.lang.NullPointerException {
    public pusta_referencja_wyjątek() { super(); }
    public pusta_referencja_wyjątek(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
