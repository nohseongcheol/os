// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;

/** 한국어로 deklarazio·던지기·잡기를 할 수 있는 S_I_salbuespen. */
public class S_I_salbuespen extends java.io.IOException {
    public S_I_salbuespen() { super(); }
    public S_I_salbuespen(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
