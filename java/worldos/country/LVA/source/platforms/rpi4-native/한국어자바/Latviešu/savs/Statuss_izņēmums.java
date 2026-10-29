// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;

/** 한국어로 deklarācija·던지기·잡기를 할 numurs 있는 Statuss_izņēmums. */
public class Statuss_izņēmums extends java.lang.IllegalStateException {
    public Statuss_izņēmums() { super(); }
    public Statuss_izņēmums(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
