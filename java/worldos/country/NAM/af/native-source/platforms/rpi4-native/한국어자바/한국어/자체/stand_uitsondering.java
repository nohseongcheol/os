// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 verklaring·던지기·잡기를 할 수 있는 stand_uitsondering. */
public class stand_uitsondering extends java.lang.IllegalStateException {
    public stand_uitsondering() { super(); }
    public stand_uitsondering(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
