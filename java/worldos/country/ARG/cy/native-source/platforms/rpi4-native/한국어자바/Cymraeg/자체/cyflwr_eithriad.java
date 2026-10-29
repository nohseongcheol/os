// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;

/** 한국어로 선언·던지기·잡기를 할 수 있는 cyflwr_eithriad. */
public class cyflwr_eithriad extends java.lang.IllegalStateException {
    public cyflwr_eithriad() { super(); }
    public cyflwr_eithriad(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
