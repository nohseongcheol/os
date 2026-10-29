// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ተጠቃሚ ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ተጠቃሚ {
    public static native int 파일서술자열기(int[] ፋይል_ምዝግብ_ስም, int ክፈት_ቅንብሮች);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int ባይት_እሴት);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ስም, int[] ውሂብ);
    public static native int ጻፍ_ቁምፊ_እሴት(int 문자);
    public static native int ጻፍ_ፋይል(int[] ስም, int[] ውሂብ, int ርዝመት_እሴት);
    public static native int መጻፊያ(String ይዘት_እሴት);
    public static native int 인수개수();
    public static native String 인수(int መረጃ_ጠቆመ);
    public static native int 실행권한();
    public static native int ክፈት_መረብ(int የአካባቢ_ወደብ);
    public static native int ላክ_ውሂብ(int እጀታ_እሴት, int አድራሻ, int መድረሻ_ወደብ, int[] ውሂብ, int ርዝመት_እሴት);
    public static native int 자료받기(int እጀታ_እሴት, int[] ውሂብ, int 제한밀리초);
    public static native int ዝጋ_መረብ(int እጀታ_እሴት);
    public static native int 내주소();
    public static native int 보낸주소(int እጀታ_እሴት);
    public static native int 보낸창구(int እጀታ_እሴት);
}
