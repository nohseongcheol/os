// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ಪರಿಕರಗಳು 전용 SVC ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು. 기존 x86 ಪರಿಕರಗಳು 원문을 함께 빌드한다. */
public final class ಬಳಕೆದಾರ {
    public static native int 파일서술자열기(int[] ಹೆಸರು, int ಸಿದ್ಧತೆಗಳು);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ಮೌಲ್ಯ);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ಹೆಸರು, int[] ಡೇಟಾ);
    public static native int ಬರೆ_ಫೈಲ್(int[] ಹೆಸರು, int[] ಡೇಟಾ, int ಉದ್ದ_ಮೌಲ್ಯ);
    public static native int ಬರೆ(String ಪಠ್ಯ);
    public static native int ಬರೆ_ಅಕ್ಷರ_ಮೌಲ್ಯ(int ಮೌಲ್ಯ);
    public static native int 인수개수();
    public static native String 인수(int ಪದಸೂಚಿ);
    public static native int 도구번호();
    public static native int 화면연결(int ಹಕ್ರಿಯೆ, int ಪದಸೂಚಿ, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ಪದಸೂಚಿ, int[] ಪಠ್ಯ, int ಉದ್ದ_ಮೌಲ್ಯ);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ಸ್ಟ್ರೀಮ್_ನಿಯಂತ್ರಣ(int ಹಕ್ರಿಯೆ, int 서술자, int ಮೌಲ್ಯ);
    public static native int ಕನೆಕ್ಟ್_ಸ್ಟ್ರೀಮ್(int 서술자, int ಇಮೇಲ್, int ಪೋರ್ಟ್_ಮೌಲ್ಯ);
    public static native int ರಚಿಸು_ನೆಟ್_ವರ್ಕ್(int ಪೋರ್ಟ್_ಮೌಲ್ಯ);
    public static native int ಕಳುಹಿಸಿ_ನೆಟ್_ವರ್ಕ್(int 서술자, int ಇಮೇಲ್, int ಪೋರ್ಟ್_ಮೌಲ್ಯ, int[] ಡೇಟಾ, int ಉದ್ದ_ಮೌಲ್ಯ);
    public static native int 통신받기(int 서술자, int[] ಡೇಟಾ, int ಉದ್ದ_ಮೌಲ್ಯ);
    public static native int ನೆಟ್_ವರ್ಕ್_ಪೋರ್ಟ್(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int ಲಂಬ_ಹುದ್ದೆ, int 폭, int 높이, int 색);
}
