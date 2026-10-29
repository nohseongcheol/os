// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti.oma;

/** 한국어로 deklaratsioon·던지기·잡기를 할 number 있는 파일없음예외. */
public class 파일없음예외 extends I_O_erand {
    public 파일없음예외() { super(); }
    public 파일없음예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
