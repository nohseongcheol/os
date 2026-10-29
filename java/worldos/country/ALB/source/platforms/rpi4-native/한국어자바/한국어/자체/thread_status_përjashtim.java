// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 deklarata·던지기·잡기를 할 수 있는 thread_status_përjashtim. */
public class thread_status_përjashtim extends java.lang.IllegalThreadStateException {
    public thread_status_përjashtim() { super(); }
    public thread_status_përjashtim(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
