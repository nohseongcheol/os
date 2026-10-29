// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuvių.savas;

/** 한국어로 deklaracija·던지기·잡기를 할 numeris 있는 배열범위예외. */
public class 배열범위예외 extends 범위예외 {
    public 배열범위예외() { super(); }
    public 배열범위예외(String aprašas) { super(aprašas); }
    public String aprašas() { return getMessage(); }
}
