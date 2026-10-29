// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 මෙවලම් 전용 SVC සම්බන්ද_වන්න. 기존 x86 මෙවලම් 원문을 함께 빌드한다. */
public final class පරිශීලක {
    public static native int 파일서술자열기(int[] නම, int සැකසුම්);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int අගය);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] නම, int[] දත්ත);
    public static native int ලියන්න_ගොනුව(int[] නම, int[] දත්ත, int දිග_අගය);
    public static native int ලිවීම(String පෙළ);
    public static native int ලියන්න_අනුලකුණ_අගය(int අගය);
    public static native int 인수개수();
    public static native String විස්තාරක(int සූචිය);
    public static native int 도구번호();
    public static native int 화면연결(int ක්_රීයාව, int සූචිය, int 가, int 나, int 다, int 라);
    public static native int 화면글(int සූචිය, int[] පෙළ, int දිග_අගය);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int දහර_පාලකය(int ක්_රීයාව, int 서술자, int අගය);
    public static native int සබඳින්න_දහර(int 서술자, int යොමුව, int තොට_අගය);
    public static native int සාදන්න_ජාලය(int තොට_අගය);
    public static native int ඊමේල්_ජාලය(int 서술자, int යොමුව, int තොට_අගය, int[] දත්ත, int දිග_අගය);
    public static native int 통신받기(int 서술자, int[] දත්ත, int දිග_අගය);
    public static native int ජාලය_තොට(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
