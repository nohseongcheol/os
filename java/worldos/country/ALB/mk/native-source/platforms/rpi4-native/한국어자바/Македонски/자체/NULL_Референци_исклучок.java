// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;

/** 한국어로 декларација·던지기·잡기를 할 수 있는 NULL_Референци_исклучок. */
public class NULL_Референци_исклучок extends java.lang.NullPointerException {
    public NULL_Референци_исклучок() { super(); }
    public NULL_Референци_исклучок(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
