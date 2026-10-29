// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;

/** 한국어로 deklarazio·던지기·잡기를 할 수 있는 salbuespen. */
public class salbuespen extends java.lang.Exception {
    public salbuespen() { super(); }
    public salbuespen(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
