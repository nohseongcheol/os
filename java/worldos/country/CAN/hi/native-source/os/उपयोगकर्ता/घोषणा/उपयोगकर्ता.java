// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros उपयोगकर्ता ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class उपयोगकर्ता {
    public static native int 파일서술자열기(int[] फ़ाइल_एन्ट्री_नाम, int जारी_सेटिंग);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int बाइट_मान);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int कमिट_फ़ाइल_संग्रहण(int 파일서술자);
    public static native int पढें_फ़ाइल(int[] नाम, int[] आँकड़े);
    public static native int लिखना_कैरेक्टर_मान(int 문자);
    public static native int लिखना_फ़ाइल(int[] नाम, int[] आँकड़े, int 길이);
    public static native int लिखें(String सामग्री_मान);
    public static native int 인수개수();
    public static native String तर्क(int इंडेक्स);
    public static native int 실행권한();
    public static native int जारी_नेटवर्क(int स्थानीय_पोर्ट);
    public static native int भेजें_डेटा(int हैंडल_मान, int पता, int गंतव्य_पोर्ट, int[] आँकड़े, int 길이);
    public static native int 자료받기(int हैंडल_मान, int[] आँकड़े, int 제한밀리초);
    public static native int बंद_नेटवर्क(int हैंडल_मान);
    public static native int 내주소();
    public static native int 보낸주소(int हैंडल_मान);
    public static native int 보낸창구(int हैंडल_मान);
}
