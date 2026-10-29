// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;

/** 한국어로 aangifte·던지기·잡기를 할 nummer 있는 I_O_uitzondering. */
public class I_O_uitzondering extends java.io.IOException {
    public I_O_uitzondering() { super(); }
    public I_O_uitzondering(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
