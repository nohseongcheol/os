// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;

/** 한국어로 선언·던지기·잡기를 할 수 있는 TYPE_Castio_eithriad. */
public class TYPE_Castio_eithriad extends java.lang.ClassCastException {
    public TYPE_Castio_eithriad() { super(); }
    public TYPE_Castio_eithriad(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
