// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros mtumiaji ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class mtumiaji {
    public static native int 파일서술자열기(int[] faili_ingizo_jina, int unda_Mipangilio);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int baiti_thamani);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Jina, int[] data);
    public static native int andika_kibambo_thamani(int 문자);
    public static native int andika_faili(int[] Jina, int[] data, int urefu_thamani);
    public static native int andika(String maudhui_thamani);
    public static native int 인수개수();
    public static native String 인수(int kielezo);
    public static native int 실행권한();
    public static native int unda_Mtandao(int jirani_kituo);
    public static native int tuma_data(int kishiko_thamani, int anwani, int fikio_kituo, int[] data, int urefu_thamani);
    public static native int 자료받기(int kishiko_thamani, int[] data, int 제한밀리초);
    public static native int funga_Mtandao(int kishiko_thamani);
    public static native int 내주소();
    public static native int 보낸주소(int kishiko_thamani);
    public static native int 보낸창구(int kishiko_thamani);
}
