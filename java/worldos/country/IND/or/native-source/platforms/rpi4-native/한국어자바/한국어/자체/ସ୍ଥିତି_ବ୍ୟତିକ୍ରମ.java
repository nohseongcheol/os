// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 선언·던지기·잡기를 할 수 있는 ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ. */
public class ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ extends java.lang.IllegalStateException {
    public ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ() { super(); }
    public ସ୍ଥିତି_ବ୍ୟତିକ୍ରମ(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
