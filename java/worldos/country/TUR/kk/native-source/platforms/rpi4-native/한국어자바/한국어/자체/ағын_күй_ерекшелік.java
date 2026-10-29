// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 мәлімдеме·던지기·잡기를 할 수 있는 ағын_күй_ерекшелік. */
public class ағын_күй_ерекшелік extends java.lang.IllegalThreadStateException {
    public ағын_күй_ерекшелік() { super(); }
    public ағын_күй_ерекшелік(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
