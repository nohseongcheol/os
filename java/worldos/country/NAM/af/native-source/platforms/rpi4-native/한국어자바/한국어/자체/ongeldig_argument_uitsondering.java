// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 verklaring·던지기·잡기를 할 수 있는 ongeldig_argument_uitsondering. */
public class ongeldig_argument_uitsondering extends java.lang.IllegalArgumentException {
    public ongeldig_argument_uitsondering() { super(); }
    public ongeldig_argument_uitsondering(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
