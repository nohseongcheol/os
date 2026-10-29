// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 പ്രസ്താവം·던지기·잡기를 할 수 있는 ഒഴിവാക്കൽ. */
public class ഒഴിവാക്കൽ extends java.lang.Exception {
    public ഒഴിവാക്കൽ() { super(); }
    public ഒഴിവാക്കൽ(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
