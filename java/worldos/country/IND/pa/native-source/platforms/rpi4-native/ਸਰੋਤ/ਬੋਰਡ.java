// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 ਮਸ਼ੀਨ 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class ਬੋਰਡ {
    public static native int 표시화소읽기(int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ);
    public static native void ਲਿੱਖੋ_ਪ੍ਰਦਰਸ਼ਨ_ਬਿੰਦੂ(int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, int 색);
    public static native int ਰਿਮੋਟ_ਨਿਯੰਤਰਣ(int 종류, int ਐਕਸ਼ਨ);
    public static native void ਅੰਤ_ਰਿਮੋਟ_ਆਦੇਸ਼(int ਸਥਿਤੀ_ਕੀਮਤ);
    public static native void 원격대기(int ਸਥਿਤੀ_ਕੀਮਤ);
    public static native void 직렬쓰기(int ਕੀਮਤ);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int ਕਾਰਵਾਈ_ਇਜਾਜ਼ਤ_ਪੱਧਰ();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ, int 색);
    public static native void ਮੁਅੱਤਲ_ਕਾਰਵਾਈ();
    public static native int ਬਣਾਓ_ਕਾਰਜ(int ਅਨੁਕ੍ਰਮਣਿਕਾ);
    public static native int ਕਾਰਜ_ਸਥਿਤੀ(int ਅਨੁਕ੍ਰਮਣਿਕਾ);
    public static native void ਰੋਕੋ(int ਸਥਿਤੀ_ਕੀਮਤ);
    public static native int 씨플러스시험();
    public static native int ਚਲਾਉ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼(int ਅਨੁਕ੍ਰਮਣਿਕਾ);
    public static native int ਚੈਕ_ਕਰੋ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼();
    public static native int 인수준비(int 개수);
    public static native int ਅਮਲ_ਕਰੋ_ਉਪਭੋਗਤਾ_ਲਿਖਤ_ਪੱਤਰ();
    public static native int 리눅스파일실행();
    public static native int ਦਲੀਲ_ਬਾਈਟ(int ਅਨੁਕ੍ਰਮਣਿਕਾ, int ਸਥਿਤੀ, int ਕੀਮਤ);
    public static native int ਟਰਮੀਨਲ(int ਐਕਸ਼ਨ);
    public static native int ਨਿਯੰਤਰਣ_ਉਪਭੋਗਤਾ_ਐਪਲੀਕੇਸ਼(int ਐਕਸ਼ਨ);
    public static native void 입출력전환(int ਐਕਸ਼ਨ);
    public static native int ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸੇਵਾ(int ਐਕਸ਼ਨ);
    public static native int ਨੈਟਵਰਕ_ਸਥਿਤੀ(int ਦਾਖਲਾ_ਕੀਮਤ, int ਅਨੁਕ੍ਰਮਣਿਕਾ);
    public static native int ਨੈਟਵਰਕ_ਸੈਟਿੰਗਾਂ(int ਐਕਸ਼ਨ, int ਪਤਾ, int ਮਾਸਕ_ਕੀਮਤ, int ਗੇਟਵੇ_ਕੀਮਤ);
    public static native int 응답보내기(int ਪਤਾ, int ਕ੍ਰਮ_ਕੀਮਤ);
    public static native int 응답읽기(int ਦਾਖਲਾ_ਕੀਮਤ);
    public static native int ਪੜਤਾਲ_ਪਰਬੰਧ(int ਦਾਖਲਾ_ਕੀਮਤ, int ਅਨੁਕ੍ਰਮਣਿਕਾ);
    public static native void 전원끄기();
}
