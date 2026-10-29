// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;

/** 한국어로 aangifte·던지기·잡기를 할 nummer 있는 nietig_argument_uitzondering. */
public class nietig_argument_uitzondering extends java.lang.IllegalArgumentException {
    public nietig_argument_uitzondering() { super(); }
    public nietig_argument_uitzondering(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
