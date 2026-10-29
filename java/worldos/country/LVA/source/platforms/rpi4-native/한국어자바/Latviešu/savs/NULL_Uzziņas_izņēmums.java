// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;

/** 한국어로 deklarācija·던지기·잡기를 할 numurs 있는 NULL_Uzziņas_izņēmums. */
public class NULL_Uzziņas_izņēmums extends java.lang.NullPointerException {
    public NULL_Uzziņas_izņēmums() { super(); }
    public NULL_Uzziņas_izņēmums(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
