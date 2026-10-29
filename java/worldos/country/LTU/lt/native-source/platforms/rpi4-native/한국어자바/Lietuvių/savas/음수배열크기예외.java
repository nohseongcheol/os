// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** 한국어로 deklaracija·던지기·잡기를 할 numeris 있는 음수배열크기예외. */
public class 음수배열크기예외 extends java.lang.NegativeArraySizeException {
    public 음수배열크기예외() { super(); }
    public 음수배열크기예외(String aprašas) { super(aprašas); }
    public String aprašas() { return getMessage(); }
}
