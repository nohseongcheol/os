// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 उपकरण 전용 SVC जोड़ना. 기존 x86 उपकरण 원문을 함께 빌드한다. */
public final class उपयोगकर्ता {
    public static native int 파일서술자열기(int[] नाम, int विन्यास);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int मान);
    public static native int 파일서술자닫기(int 서술자);
    public static native int पढें_फ़ाइल(int[] नाम, int[] आँकड़े);
    public static native int लिखना_फ़ाइल(int[] नाम, int[] आँकड़े, int 길이);
    public static native int लिखें(String पाठ);
    public static native int लिखना_कैरेक्टर_मान(int मान);
    public static native int 인수개수();
    public static native String तर्क(int इंडेक्स);
    public static native int 도구번호();
    public static native int 화면연결(int क्रिया, int इंडेक्स, int 가, int 나, int 다, int 라);
    public static native int 화면글(int इंडेक्स, int[] पाठ, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int स्ट्रीम_नियंत्रण(int क्रिया, int 서술자, int मान);
    public static native int कनेक्ट_स्ट्रीम(int 서술자, int पता, int पोर्ट_मान);
    public static native int जारी_नेटवर्क(int पोर्ट_मान);
    public static native int भेजें_नेटवर्क(int 서술자, int पता, int पोर्ट_मान, int[] आँकड़े, int 길이);
    public static native int 통신받기(int 서술자, int[] आँकड़े, int 길이);
    public static native int नेटवर्क_पोर्ट(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int रेक्_टेंगल(int 가로, int अनुलंब_पद, int 폭, int 높이, int 색);
}
