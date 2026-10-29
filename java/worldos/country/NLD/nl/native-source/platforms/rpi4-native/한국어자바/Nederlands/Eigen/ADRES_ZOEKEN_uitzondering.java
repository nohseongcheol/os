// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Nederlands.Eigen;

/** 한국어로 aangifte·던지기·잡기를 할 nummer 있는 ADRES_ZOEKEN_uitzondering. */
public class ADRES_ZOEKEN_uitzondering extends I_O_uitzondering {
    public ADRES_ZOEKEN_uitzondering() { super(); }
    public ADRES_ZOEKEN_uitzondering(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
