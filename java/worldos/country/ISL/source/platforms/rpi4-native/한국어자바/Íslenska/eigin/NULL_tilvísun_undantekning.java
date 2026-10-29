// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Íslenska.eigin;

/** 한국어로 skýrsla·던지기·잡기를 할 númer 있는 NULL_tilvísun_undantekning. */
public class NULL_tilvísun_undantekning extends java.lang.NullPointerException {
    public NULL_tilvísun_undantekning() { super(); }
    public NULL_tilvísun_undantekning(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
