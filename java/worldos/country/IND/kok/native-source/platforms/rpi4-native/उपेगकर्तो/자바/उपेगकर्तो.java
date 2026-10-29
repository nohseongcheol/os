// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 साधनां 전용 SVC कनॅक्ट. 기존 x86 साधनां 원문을 함께 빌드한다. */
public final class उपेगकर्तो {
    public static native int 파일서술자열기(int[] नांव, int मांडावळी);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int मोल);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] नांव, int[] डेटा);
    public static native int बरोवचें_फायल(int[] नांव, int[] डेटा, int लांबाय_मोल);
    public static native int बरोवचें(String SMS);
    public static native int बरोवचें_वर्ण_मोल(int मोल);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int कृती, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] SMS, int लांबाय_मोल);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_नियंत्रण(int कृती, int 서술자, int मोल);
    public static native int कनॅक्ट_Stream(int 서술자, int नामो, int पोर्ट_मोल);
    public static native int उगडचें_नॅटवर्क(int पोर्ट_मोल);
    public static native int धाडचें_नॅटवर्क(int 서술자, int नामो, int पोर्ट_मोल, int[] डेटा, int लांबाय_मोल);
    public static native int 통신받기(int 서술자, int[] डेटा, int लांबाय_मोल);
    public static native int नॅटवर्क_पोर्ट(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int उबें_स्थिती, int 폭, int 높이, int 색);
}
