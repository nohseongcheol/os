// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;

/** 한국어로 deklarasi_4f4f026b·던지기·잡기를 할 수 있는 pengecualian. */
public class pengecualian extends java.lang.Exception {
    public pengecualian() { super(); }
    public pengecualian(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
