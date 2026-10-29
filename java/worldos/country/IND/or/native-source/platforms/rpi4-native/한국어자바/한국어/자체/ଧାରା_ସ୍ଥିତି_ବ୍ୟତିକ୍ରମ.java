// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 선언·던지기·잡기를 할 수 있는 ଧାରା_ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ. */
public class ଧାରା_ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ extends java.lang.IllegalThreadStateException {
    public ଧାରା_ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ() { super(); }
    public ଧାରା_ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
