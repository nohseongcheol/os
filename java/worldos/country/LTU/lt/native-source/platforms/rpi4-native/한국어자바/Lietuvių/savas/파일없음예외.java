// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** 한국어로 deklaracija·던지기·잡기를 할 numeris 있는 파일없음예외. */
public class 파일없음예외 extends Į_I_išimtis {
    public 파일없음예외() { super(); }
    public 파일없음예외(String aprašas) { super(aprašas); }
    public String aprašas() { return getMessage(); }
}
