// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 e_lon_qilish·던지기·잡기를 할 수 있는 I_O_istisno. */
public class I_O_istisno extends java.io.IOException {
    public I_O_istisno() { super(); }
    public I_O_istisno(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
