// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros प्रयोगकर्ता ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class प्रयोगकर्ता {
    public static native int 파일서술자열기(int[] फाइल_प्रविष्टि_नाम, int सिर्जना_सेटिङहरू);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int बाइट_मान);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] नाम, int[] लगत);
    public static native int लेख्नुहोस्_वर्ण_मान(int 문자);
    public static native int लेख्नुहोस्_फाइल(int[] नाम, int[] लगत, int लम्बाइ_मान);
    public static native int लेख्नुहोस्(String सामग्री_मान);
    public static native int 인수개수();
    public static native String तर्क(int अनुक्रमणिका);
    public static native int 실행권한();
    public static native int सिर्जना_सञ्जाल(int स्थानीय_पोर्ट);
    public static native int पठाउनुहोस्_लगत(int ह्यान्डल_मान, int ठेगाना, int गन्तव्य_पोर्ट, int[] लगत, int लम्बाइ_मान);
    public static native int 자료받기(int ह्यान्डल_मान, int[] लगत, int 제한밀리초);
    public static native int बन्द_गर्नुहोस्_सञ्जाल(int ह्यान्डल_मान);
    public static native int 내주소();
    public static native int 보낸주소(int ह्यान्डल_मान);
    public static native int 보낸창구(int ह्यान्डल_मान);
}
