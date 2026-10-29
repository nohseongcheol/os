// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;

/** 한국어로 deklarazio·던지기·잡기를 할 수 있는 baliogabe_arg_salbuespen. */
public class baliogabe_arg_salbuespen extends java.lang.IllegalArgumentException {
    public baliogabe_arg_salbuespen() { super(); }
    public baliogabe_arg_salbuespen(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
