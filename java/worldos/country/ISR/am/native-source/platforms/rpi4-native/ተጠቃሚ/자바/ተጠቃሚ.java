// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 መሳሪያዎች 전용 SVC መገናኛ. 기존 x86 መሳሪያዎች 원문을 함께 빌드한다. */
public final class ተጠቃሚ {
    public static native int 파일서술자열기(int[] ስም, int ማሰናጃዎች);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int እሴት);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ስም, int[] ውሂብ);
    public static native int ጻፍ_ፋይል(int[] ስም, int[] ውሂብ, int ርዝመት_እሴት);
    public static native int መጻፊያ(String ጽሁፍ);
    public static native int ጻፍ_ቁምፊ_እሴት(int እሴት);
    public static native int 인수개수();
    public static native String 인수(int መረጃ_ጠቆመ);
    public static native int 도구번호();
    public static native int 화면연결(int ተግባር, int መረጃ_ጠቆመ, int 가, int 나, int 다, int 라);
    public static native int 화면글(int መረጃ_ጠቆመ, int[] ጽሁፍ, int ርዝመት_እሴት);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ልቀቅ_ቁጥጥር(int ተግባር, int 서술자, int እሴት);
    public static native int አገናኝ_ልቀቅ(int 서술자, int አድራሻ, int ወደብ_እሴት);
    public static native int ክፈት_መረብ(int ወደብ_እሴት);
    public static native int ላክ_መረብ(int 서술자, int አድራሻ, int ወደብ_እሴት, int[] ውሂብ, int ርዝመት_እሴት);
    public static native int 통신받기(int 서술자, int[] ውሂብ, int ርዝመት_እሴት);
    public static native int መረብ_ወደብ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int ቋሚ_በቦታ_አስቀመጠ, int 폭, int 높이, int 색);
}
