// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 tamko·던지기·잡기를 할 수 있는 batili_hoja_vighairi. */
public class batili_hoja_vighairi extends java.lang.IllegalArgumentException {
    public batili_hoja_vighairi() { super(); }
    public batili_hoja_vighairi(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
