// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 declaration·던지기·잡기를 할 수 있는 thread_katayuan_pagbubukod. */
public class thread_katayuan_pagbubukod extends java.lang.IllegalThreadStateException {
    public thread_katayuan_pagbubukod() { super(); }
    public thread_katayuan_pagbubukod(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
