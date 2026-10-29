// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 한국어로 ప్రకటన·던지기·잡기를 할 수 있는 మూ_ఫ_మినహాయింపు. */
public class మూ_ఫ_మినహాయింపు extends java.io.IOException {
    public మూ_ఫ_మినహాయింపు() { super(); }
    public మూ_ఫ_మినహాయింపు(String 설명) { super(설명); }
    public String 설명() { return getMessage(); }
}
