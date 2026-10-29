// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ਸਾਧਨ 전용 SVC ਕੁਨੈਕਸ਼ਨ_ਕਰੋ. 기존 x86 ਸਾਧਨ 원문을 함께 빌드한다. */
public final class ਉਪਭੋਗਤਾ {
    public static native int 파일서술자열기(int[] ਨਾਂ, int ਸੈਟਿੰਗ);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ਕੀਮਤ);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ਨਾਂ, int[] ਸਮੱਗਰੀ);
    public static native int ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ(int[] ਨਾਂ, int[] ਸਮੱਗਰੀ, int ਲੰਬਾਈ_ਕੀਮਤ);
    public static native int ਲਿਖਣ(String ਟੈਕਸਟ);
    public static native int ਲਿੱਖੋ_ਵਰਣ_ਕੀਮਤ(int ਕੀਮਤ);
    public static native int 인수개수();
    public static native String ਆਰਗੂਮੈਂਟ(int ਅਨੁਕ੍ਰਮਣਿਕਾ);
    public static native int 도구번호();
    public static native int 화면연결(int ਐਕਸ਼ਨ, int ਅਨੁਕ੍ਰਮਣਿਕਾ, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ਅਨੁਕ੍ਰਮਣਿਕਾ, int[] ਟੈਕਸਟ, int ਲੰਬਾਈ_ਕੀਮਤ);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ਸਟ੍ਰੀਮ_ਨਿਯੰਤਰਣ(int ਐਕਸ਼ਨ, int 서술자, int ਕੀਮਤ);
    public static native int ਕਨੈਕਟ_ਕਰੋ_ਸਟ੍ਰੀਮ(int 서술자, int ਪਤਾ, int ਪੋਰਟ_ਕੀਮਤ);
    public static native int ਖੋਲੋ_ਨੈਟਵਰਕ(int ਪੋਰਟ_ਕੀਮਤ);
    public static native int ਈਮੇਲ_ਨੈਟਵਰਕ(int 서술자, int ਪਤਾ, int ਪੋਰਟ_ਕੀਮਤ, int[] ਸਮੱਗਰੀ, int ਲੰਬਾਈ_ਕੀਮਤ);
    public static native int 통신받기(int 서술자, int[] ਸਮੱਗਰੀ, int ਲੰਬਾਈ_ਕੀਮਤ);
    public static native int ਨੈਟਵਰਕ_ਪੋਰਟ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, int 폭, int 높이, int 색);
}
