// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros उपेगकर्तो ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class उपेगकर्तो {
    public static native int 파일서술자열기(int[] फायल_प्रवेश_नांव, int उगडचें_मांडावळी);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int बायट_मोल);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] नांव, int[] डेटा);
    public static native int बरोवचें_वर्ण_मोल(int 문자);
    public static native int बरोवचें_फायल(int[] नांव, int[] डेटा, int लांबाय_मोल);
    public static native int बरोवचें(String अनुक्रमणिका_मोल);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int उगडचें_नॅटवर्क(int थळावो_पोर्ट);
    public static native int धाडचें_डेटा(int हँडल_मोल, int नामो, int नियुक्त_स्थान_पोर्ट, int[] डेटा, int लांबाय_मोल);
    public static native int 자료받기(int हँडल_मोल, int[] डेटा, int 제한밀리초);
    public static native int शेवट_नॅटवर्क(int हँडल_मोल);
    public static native int 내주소();
    public static native int 보낸주소(int हँडल_मोल);
    public static native int 보낸창구(int हँडल_मोल);
}
