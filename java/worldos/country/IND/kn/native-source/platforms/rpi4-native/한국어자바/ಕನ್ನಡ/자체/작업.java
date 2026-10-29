// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಕನ್ನಡ.자체;
/** 작업 ಎಳೆ_ಮೌಲ್ಯ: 하나의 ಪೂರೈಸು_ಆದೇಶ ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ. 자체 JVM 안에서 ಆಜ್ಞೆ 수를 기준으로 번갈아 실행한다. */
public final class 작업 {
    private 작업() {}
    public static 작업가닥 ಚಲಾಯಿಸು_2(실행할일 ಕಾರ್ಯ_ಕ್ರಿಯೆ) { 작업가닥 ಎಳೆ_ಮೌಲ್ಯ = new 작업가닥(ಕಾರ್ಯ_ಕ್ರಿಯೆ); ಎಳೆ_ಮೌಲ್ಯ.ಆರಂಭಿಸು_ಕಾರ್ಯ(); return ಎಳೆ_ಮೌಲ್ಯ; }
    public static void 기다리기(작업가닥 ಎಳೆ_ಮೌಲ್ಯ) throws 대기중단예외 { ಎಳೆ_ಮೌಲ್ಯ.기다리기(); }
    public static boolean 살아있는가(작업가닥 ಎಳೆ_ಮೌಲ್ಯ) { return ಎಳೆ_ಮೌಲ್ಯ.살아있는가(); }
    public static void ಸ್ಥಗಿತಗೊಳಿಸಲಾಗಿದೆ_ಕಾರ್ಯ() { 작업가닥.ಸ್ಥಗಿತಗೊಳಿಸಲಾಗಿದೆ_ಕಾರ್ಯ(); }
}
