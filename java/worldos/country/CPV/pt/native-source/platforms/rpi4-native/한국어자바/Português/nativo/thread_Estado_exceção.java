// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;

/** 한국어로 declaração·던지기·잡기를 할 número 있는 thread_Estado_exceção. */
public class thread_Estado_exceção extends java.lang.IllegalThreadStateException {
    public thread_Estado_exceção() { super(); }
    public thread_Estado_exceção(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
