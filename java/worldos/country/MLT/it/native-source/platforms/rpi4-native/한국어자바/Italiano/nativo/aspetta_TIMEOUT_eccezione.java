// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;

/** 한국어로 dichiarazione·던지기·잡기를 할 numero 있는 aspetta_TIMEOUT_eccezione. */
public class aspetta_TIMEOUT_eccezione extends I_O_eccezione {
    public aspetta_TIMEOUT_eccezione() { super(); }
    public aspetta_TIMEOUT_eccezione(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
