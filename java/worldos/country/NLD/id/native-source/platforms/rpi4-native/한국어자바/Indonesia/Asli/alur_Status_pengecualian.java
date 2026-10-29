// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;

/** 한국어로 deklarasi_4f4f026b·던지기·잡기를 할 수 있는 alur_Status_pengecualian. */
public class alur_Status_pengecualian extends java.lang.IllegalThreadStateException {
    public alur_Status_pengecualian() { super(); }
    public alur_Status_pengecualian(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
