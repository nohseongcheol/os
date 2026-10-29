// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 абвяшчэнне·던지기·잡기를 할 수 있는 памылковы_аргумент_выключэнне. */
public class памылковы_аргумент_выключэнне extends java.lang.IllegalArgumentException {
    public памылковы_аргумент_выключэнне() { super(); }
    public памылковы_аргумент_выключэнне(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
