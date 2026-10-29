// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;

/** 한국어로 deklaracija·던지기·잡기를 할 수 있는 숫자형식예외. */
public class 숫자형식예외 extends nevaljan_argument_iznimka {
    public 숫자형식예외() { super(); }
    public 숫자형식예외(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
