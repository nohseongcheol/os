// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 мәлімдеме·던지기·잡기를 할 수 있는 ерекшелік. */
public class ерекшелік extends java.lang.Exception {
    public ерекшелік() { super(); }
    public ерекшелік(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
