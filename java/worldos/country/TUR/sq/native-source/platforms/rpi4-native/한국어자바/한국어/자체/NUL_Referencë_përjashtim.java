// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 deklarata·던지기·잡기를 할 수 있는 NUL_Referencë_përjashtim. */
public class NUL_Referencë_përjashtim extends java.lang.NullPointerException {
    public NUL_Referencë_përjashtim() { super(); }
    public NUL_Referencë_përjashtim(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
