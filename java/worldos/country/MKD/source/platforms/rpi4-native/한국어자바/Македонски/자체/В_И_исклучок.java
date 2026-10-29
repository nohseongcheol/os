// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Македонски.자체;

/** 한국어로 декларација·던지기·잡기를 할 수 있는 В_И_исклучок. */
public class В_И_исклучок extends java.io.IOException {
    public В_И_исклучок() { super(); }
    public В_И_исклучок(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
