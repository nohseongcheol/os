// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 ಯಂತ್ರ 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class ಬೋರ್ಡ್ {
    public static native int 표시화소읽기(int 가로, int ಲಂಬ_ಹುದ್ದೆ);
    public static native void ಬರೆ_ಪ್ರದರ್ಶನ_ಪೆಲ್(int 가로, int ಲಂಬ_ಹುದ್ದೆ, int 색);
    public static native int ಶಾಡೋಯಿಂಗ್(int 종류, int ಹಕ್ರಿಯೆ);
    public static native void ಅಂತ್ಯಗೊಳಿಸು_ರಿಮೋಟ್_ಆದೇಶ(int ಸ್ಥಿತಿ_ಮೌಲ್ಯ);
    public static native void ರಿಮೋಟ್_ನಿರೀಕ್ಷಣೆ(int ಸ್ಥಿತಿ_ಮೌಲ್ಯ);
    public static native void 직렬쓰기(int ಮೌಲ್ಯ);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int ಪ್ರಾಸೆಸರ್_ಅನುಮತಿ_ಹಂತ();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int ಲಂಬ_ಹುದ್ದೆ, int 색);
    public static native void ಸ್ಥಗಿತಗೊಳಿಸಲಾಗಿದೆ_ಸಂಸ್ಕಾರಕ();
    public static native int ರಚಿಸು_ಕಾರ್ಯ(int ಪದಸೂಚಿ);
    public static native int ಕಾರ್ಯ_ಸ್ಥಿತಿ(int ಪದಸೂಚಿ);
    public static native void ನಿಲ್ಲು(int ಸ್ಥಿತಿ_ಮೌಲ್ಯ);
    public static native int 씨플러스시험();
    public static native int ಚಲನೆ_ಬಳಕೆದಾರ_ಅಪ್ಲಿ(int ಪದಸೂಚಿ);
    public static native int ಚೆಕ್_ಬಳಕೆದಾರ_ಅಪ್ಲಿ();
    public static native int 인수준비(int 개수);
    public static native int ಪೂರೈಸು_ಬಳಕೆದಾರ_ಫೈಲ್();
    public static native int 리눅스파일실행();
    public static native int ವಾದ_ಬೈಟ್(int ಪದಸೂಚಿ, int ಸ್ಥಾನ, int ಮೌಲ್ಯ);
    public static native int ಟರ್ಮಿನಲ್(int ಹಕ್ರಿಯೆ);
    public static native int ನಿಯಂತ್ರಣ_ಬಳಕೆದಾರ_ಅಪ್ಲಿ(int ಹಕ್ರಿಯೆ);
    public static native void 입출력전환(int ಹಕ್ರಿಯೆ);
    public static native int ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸೇವಾ(int ಹಕ್ರಿಯೆ);
    public static native int ನೆಟ್_ವರ್ಕ್_ಲಭ್ಯತೆ(int ನಮೂದು_ಮೌಲ್ಯ, int ಪದಸೂಚಿ);
    public static native int ನೆಟ್_ವರ್ಕ್_ಸೆಟ್ಟಿಂಗ್ಸ್(int ಹಕ್ರಿಯೆ, int ಇಮೇಲ್, int ಮುಖವಾಡ_ಮೌಲ್ಯ, int ಗೇಟ್_ವೇ_ಮೌಲ್ಯ);
    public static native int 응답보내기(int ಇಮೇಲ್, int ಕ್ರಮ_ಮೌಲ್ಯ);
    public static native int 응답읽기(int ನಮೂದು_ಮೌಲ್ಯ);
    public static native int ಪ್ರಶ್ನಾವಳಿ_ಸಿಸ್ಟಂ(int ನಮೂದು_ಮೌಲ್ಯ, int ಪದಸೂಚಿ);
    public static native void 전원끄기();
}
