// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;

/** 작업 자체의 종료가 아니라, 가닥을 기다리던 동작의 중단을 나타낸다. */
public class 대기중단예외 extends java.lang.InterruptedException {
    public 대기중단예외() { super(); }
    public 대기중단예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
