// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 ማሽን 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void ጸሓፍ_መርኣዪ_ንጣብ(int 가로, int 세로, int 색);
    public static native int ጽላሎት(int 종류, int ስጉምቲ);
    public static native void ኣቑም_ርሑቕ_ትእዛዝ(int ደረጃ_ዋጋ);
    public static native void 원격대기(int ደረጃ_ዋጋ);
    public static native void 직렬쓰기(int ዋጋ);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void አግድ_ፕሮሰሰር();
    public static native int ፍጠር_ዕማም(int መሐበሪ);
    public static native int ዕማም_ደረጃ(int መሐበሪ);
    public static native void ኣቑም(int ደረጃ_ዋጋ);
    public static native int 씨플러스시험();
    public static native int ኣኺድ_ተጠቃሚ_መተግበሪ(int መሐበሪ);
    public static native int ፈትሽ_ተጠቃሚ_መተግበሪ();
    public static native int 인수준비(int 개수);
    public static native int ተግብር_ተጠቃሚ_ፋይል();
    public static native int 리눅스파일실행();
    public static native int ሓባሪ_ቁጽሪ_ባይት(int መሐበሪ, int 위치, int ዋጋ);
    public static native int 터미널(int ስጉምቲ);
    public static native int ቁጽጽር_ተጠቃሚ_መተግበሪ(int ስጉምቲ);
    public static native void 입출력전환(int ስጉምቲ);
    public static native int ፋይል_ምስጋር_ኣገልግሎት(int ስጉምቲ);
    public static native int ማሕበራዊ_ኔትወርክ_ደረጃ(int ምእታው_ዋጋ, int መሐበሪ);
    public static native int ማሕበራዊ_ኔትወርክ_ኣቀማምጣታት(int ስጉምቲ, int ኣድራሻ, int 가림, int 관문);
    public static native int 응답보내기(int ኣድራሻ, int ተርታ_ዋጋ);
    public static native int 응답읽기(int ምእታው_ዋጋ);
    public static native int ሕቶ_ስርዓት(int ምእታው_ዋጋ, int መሐበሪ);
    public static native void 전원끄기();
}
