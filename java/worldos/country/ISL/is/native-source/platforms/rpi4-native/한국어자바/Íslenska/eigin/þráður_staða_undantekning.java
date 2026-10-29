// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;

/** 한국어로 skýrsla·던지기·잡기를 할 númer 있는 þráður_staða_undantekning. */
public class þráður_staða_undantekning extends java.lang.IllegalThreadStateException {
    public þráður_staða_undantekning() { super(); }
    public þráður_staða_undantekning(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
