// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;

/** 한국어로 እወጃ·던지기·잡기를 할 수 있는 ዞን_ልዩነት. */
public class ዞን_ልዩነት extends java.lang.IllegalStateException {
    public ዞን_ልዩነት() { super(); }
    public ዞን_ልዩነት(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
