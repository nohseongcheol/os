// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 абвяшчэнне·던지기·잡기를 할 수 있는 увод_вывад_выключэнне. */
public class увод_вывад_выключэнне extends java.io.IOException {
    public увод_вывад_выключэнне() { super(); }
    public увод_вывад_выключэнне(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
