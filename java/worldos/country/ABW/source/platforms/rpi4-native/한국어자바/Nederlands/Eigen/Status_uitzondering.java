// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;

/** 한국어로 aangifte·던지기·잡기를 할 nummer 있는 Status_uitzondering. */
public class Status_uitzondering extends java.lang.IllegalStateException {
    public Status_uitzondering() { super(); }
    public Status_uitzondering(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
