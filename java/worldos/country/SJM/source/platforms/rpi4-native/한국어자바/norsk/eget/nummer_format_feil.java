// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package norsk.eget;

/** 한국어로 erklæring·던지기·잡기를 할 nummer 있는 nummer_format_feil. */
public class nummer_format_feil extends ugyldig_argument_unntak {
    public nummer_format_feil() { super(); }
    public nummer_format_feil(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
