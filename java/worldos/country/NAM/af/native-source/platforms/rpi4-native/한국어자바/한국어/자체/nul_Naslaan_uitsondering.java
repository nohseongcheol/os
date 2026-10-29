// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 verklaring·던지기·잡기를 할 수 있는 nul_Naslaan_uitsondering. */
public class nul_Naslaan_uitsondering extends java.lang.NullPointerException {
    public nul_Naslaan_uitsondering() { super(); }
    public nul_Naslaan_uitsondering(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
