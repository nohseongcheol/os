// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package हिंदी.निज;

/** 한국어로 घोषणा·던지기·잡기를 할 수 있는 अवस्था_अपवाद. */
public class अवस्था_अपवाद extends java.lang.IllegalStateException {
    public अवस्था_अपवाद() { super(); }
    public अवस्था_अपवाद(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
