// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ተጠቃሚ ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ተጠቃሚ {
    public static native int 파일서술자열기(int[] ፋይል_ምእታው_ሽም, int ክፈት_ኣቀማምጣታት);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int ባይት_ዋጋ);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] ሽም, int[] ሓበሬታ);
    public static native int ጸሓፍ_ፊደል_ዋጋ(int 문자);
    public static native int ጸሓፍ_ፋይል(int[] ሽም, int[] ሓበሬታ, int ንውሓት_ዋጋ);
    public static native int ጸሓፍ(String ትሕዝቶ_ዋጋ);
    public static native int 인수개수();
    public static native String 인수(int መሐበሪ);
    public static native int 실행권한();
    public static native int ክፈት_ማሕበራዊ_ኔትወርክ(int ኣካባብያዊ_ወደብ);
    public static native int ለኣኽ_ሓበሬታ(int መትሓዚ_ዋጋ, int ኣድራሻ, int መዓልቦ_ወደብ, int[] ሓበሬታ, int ንውሓት_ዋጋ);
    public static native int 자료받기(int መትሓዚ_ዋጋ, int[] ሓበሬታ, int 제한밀리초);
    public static native int ዕጸው_ማሕበራዊ_ኔትወርክ(int መትሓዚ_ዋጋ);
    public static native int 내주소();
    public static native int 보낸주소(int መትሓዚ_ዋጋ);
    public static native int 보낸창구(int መትሓዚ_ዋጋ);
}
