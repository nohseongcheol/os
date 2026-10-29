// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 абвяшчэнне·던지기·잡기를 할 수 있는 주소확인예외. */
public class 주소확인예외 extends увод_вывад_выключэнне {
    public 주소확인예외() { super(); }
    public 주소확인예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
