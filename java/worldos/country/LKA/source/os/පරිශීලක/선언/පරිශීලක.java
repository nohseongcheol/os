// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros පරිශීලක ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class පරිශීලක {
    public static native int 파일서술자열기(int[] ගොනුව_පිවිසුම_නම, int සාදන්න_පසුතල);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int බයිටය_අගය);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] නම, int[] දත්ත);
    public static native int ලියන්න_අනුලකුණ_අගය(int 문자);
    public static native int ලියන්න_ගොනුව(int[] නම, int[] දත්ත, int දිග_අගය);
    public static native int ලිවීම(String අන්තර්ගතය_අගය);
    public static native int 인수개수();
    public static native String විස්තාරක(int සූචිය);
    public static native int 실행권한();
    public static native int සාදන්න_ජාලය(int ස්ව_තොට);
    public static native int ඊමේල්_දත්ත(int හසුරුව_අගය, int යොමුව, int ගමනාන්තය_තොට, int[] දත්ත, int දිග_අගය);
    public static native int 자료받기(int හසුරුව_අගය, int[] දත්ත, int 제한밀리초);
    public static native int වසන්න_ජාලය(int හසුරුව_අගය);
    public static native int 내주소();
    public static native int 보낸주소(int හසුරුව_අගය);
    public static native int 보낸창구(int හසුරුව_අගය);
}
