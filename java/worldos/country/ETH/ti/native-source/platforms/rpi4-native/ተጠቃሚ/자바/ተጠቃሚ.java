// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 መሳርሒታት 전용 SVC ኣላግብ. 기존 x86 መሳርሒታት 원문을 함께 빌드한다. */
public final class ተጠቃሚ {
    public static native int 파일서술자열기(int[] ሽም, int ኣቀማምጣታት);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int ዋጋ);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ሽም, int[] ሓበሬታ);
    public static native int ጸሓፍ_ፋይል(int[] ሽም, int[] ሓበሬታ, int ንውሓት_ዋጋ);
    public static native int ጸሓፍ(String ጽሑፍ);
    public static native int ጸሓፍ_ፊደል_ዋጋ(int ዋጋ);
    public static native int 인수개수();
    public static native String 인수(int መሐበሪ);
    public static native int 도구번호();
    public static native int 화면연결(int ስጉምቲ, int መሐበሪ, int 가, int 나, int 다, int 라);
    public static native int 화면글(int መሐበሪ, int[] ጽሑፍ, int ንውሓት_ዋጋ);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ወሓዚ_ቁጽጽር(int ስጉምቲ, int 서술자, int ዋጋ);
    public static native int ኣላግብ_ወሓዚ(int 서술자, int ኣድራሻ, int ወደብ_ዋጋ);
    public static native int ክፈት_ማሕበራዊ_ኔትወርክ(int ወደብ_ዋጋ);
    public static native int ለኣኽ_ማሕበራዊ_ኔትወርክ(int 서술자, int ኣድራሻ, int ወደብ_ዋጋ, int[] ሓበሬታ, int ንውሓት_ዋጋ);
    public static native int 통신받기(int 서술자, int[] ሓበሬታ, int ንውሓት_ዋጋ);
    public static native int ማሕበራዊ_ኔትወርክ_ወደብ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
