// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package hrvatski.vlastiti;

/** 한국어로 deklaracija·던지기·잡기를 할 수 있는 NULL_Reference_iznimka. */
public class NULL_Reference_iznimka extends java.lang.NullPointerException {
    public NULL_Reference_iznimka() { super(); }
    public NULL_Reference_iznimka(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
