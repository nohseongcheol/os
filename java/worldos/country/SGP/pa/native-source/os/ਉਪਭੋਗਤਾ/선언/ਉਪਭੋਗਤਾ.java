// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ਉਪਭੋਗਤਾ ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ਉਪਭੋਗਤਾ {
    public static native int 파일서술자열기(int[] ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ, int ਖੋਲੋ_ਸੈਟਿੰਗਾਂ);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int ਬਾਈਟ_ਕੀਮਤ);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ਨਾਂ, int[] ਸਮੱਗਰੀ);
    public static native int ਲਿੱਖੋ_ਵਰਣ_ਕੀਮਤ(int 문자);
    public static native int ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ(int[] ਨਾਂ, int[] ਸਮੱਗਰੀ, int ਲੰਬਾਈ_ਕੀਮਤ);
    public static native int ਲਿਖਣ(String ਤਤਕਰਾ_ਕੀਮਤ);
    public static native int 인수개수();
    public static native String ਆਰਗੂਮੈਂਟ(int ਅਨੁਕ੍ਰਮਣਿਕਾ);
    public static native int 실행권한();
    public static native int ਖੋਲੋ_ਨੈਟਵਰਕ(int ਲੋਕਲ_ਪੋਰਟ);
    public static native int ਈਮੇਲ_ਸਮੱਗਰੀ(int ਸੰਭਾਲਣਾ_ਕੀਮਤ, int ਪਤਾ, int ਮੰਜਿਲ_ਪੋਰਟ, int[] ਸਮੱਗਰੀ, int ਲੰਬਾਈ_ਕੀਮਤ);
    public static native int 자료받기(int ਸੰਭਾਲਣਾ_ਕੀਮਤ, int[] ਸਮੱਗਰੀ, int 제한밀리초);
    public static native int ਬੰਦ_ਕਰੋ_ਨੈਟਵਰਕ(int ਸੰਭਾਲਣਾ_ਕੀਮਤ);
    public static native int 내주소();
    public static native int 보낸주소(int ਸੰਭਾਲਣਾ_ਕੀਮਤ);
    public static native int 보낸창구(int ਸੰਭਾਲਣਾ_ਕੀਮਤ);
}
