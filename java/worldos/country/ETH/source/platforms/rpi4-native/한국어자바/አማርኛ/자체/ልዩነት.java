// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;

/** 한국어로 እወጃ·던지기·잡기를 할 수 있는 ልዩነት. */
public class ልዩነት extends java.lang.Exception {
    public ልዩነት() { super(); }
    public ልዩነት(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
