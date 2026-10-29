// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gaeilge.자체;

/** 한국어로 선언·던지기·잡기를 할 수 있는 neamhbhailí_argóint_eisceacht. */
public class neamhbhailí_argóint_eisceacht extends java.lang.IllegalArgumentException {
    public neamhbhailí_argóint_eisceacht() { super(); }
    public neamhbhailí_argóint_eisceacht(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
