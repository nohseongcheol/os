// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ಬಳಕೆದಾರ ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ಬಳಕೆದಾರ {
    public static native int 파일서술자열기(int[] ಫೈಲ್_ನಮೂದು_ಹೆಸರು, int ರಚಿಸು_ಸೆಟ್ಟಿಂಗ್ಸ್);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int ಬೈಟ್_ಮೌಲ್ಯ);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ಹೆಸರು, int[] ಡೇಟಾ);
    public static native int ಬರೆ_ಅಕ್ಷರ_ಮೌಲ್ಯ(int 문자);
    public static native int ಬರೆ_ಫೈಲ್(int[] ಹೆಸರು, int[] ಡೇಟಾ, int ಉದ್ದ_ಮೌಲ್ಯ);
    public static native int ಬರೆ(String ವಿಷಯ_ಮೌಲ್ಯ);
    public static native int 인수개수();
    public static native String 인수(int ಪದಸೂಚಿ);
    public static native int 실행권한();
    public static native int ರಚಿಸು_ನೆಟ್_ವರ್ಕ್(int ಸ್ಥಳೀಯ_ಪೋರ್ಟ್);
    public static native int ಕಳುಹಿಸಿ_ಡೇಟಾ(int ಹ್ಯಾಂಡಲ್_ಮೌಲ್ಯ, int ಇಮೇಲ್, int ಗಮ್ಯಸ್ಥಾನ_ಪೋರ್ಟ್, int[] ಡೇಟಾ, int ಉದ್ದ_ಮೌಲ್ಯ);
    public static native int 자료받기(int ಹ್ಯಾಂಡಲ್_ಮೌಲ್ಯ, int[] ಡೇಟಾ, int 제한밀리초);
    public static native int ಮುಚ್ಚು_ನೆಟ್_ವರ್ಕ್(int ಹ್ಯಾಂಡಲ್_ಮೌಲ್ಯ);
    public static native int 내주소();
    public static native int 보낸주소(int ಹ್ಯಾಂಡಲ್_ಮೌಲ್ಯ);
    public static native int 보낸창구(int ಹ್ಯಾಂಡಲ್_ಮೌಲ್ಯ);
}
