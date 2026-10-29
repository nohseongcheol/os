// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;

/** 한국어로 घोषणा·던지기·잡기를 할 수 있는 अमान्य_तर्क_अपवाद. */
public class अमान्य_तर्क_अपवाद extends java.lang.IllegalArgumentException {
    public अमान्य_तर्क_अपवाद() { super(); }
    public अमान्य_तर्क_अपवाद(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
