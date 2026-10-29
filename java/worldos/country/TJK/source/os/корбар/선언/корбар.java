// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros корбар ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class корбар {
    public static native int 파일서술자열기(int[] файл_ворида_ном, int кушодан_Танзимот);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int байт_қимат);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Ном, int[] иттилоот);
    public static native int навиштан_аломат_қимат(int 문자);
    public static native int навиштан_файл(int[] Ном, int[] иттилоот, int дарозӣ_қимат);
    public static native int Навиштан(String Мӯҳтаво_қимат);
    public static native int 인수개수();
    public static native String 인수(int индекс);
    public static native int 실행권한();
    public static native int кушодан_Шабака(int маҳаллӣ_порт);
    public static native int фиристодан_иттилоот(int дастак_қимат, int суроға, int ҷои_таъинот_порт, int[] иттилоот, int дарозӣ_қимат);
    public static native int 자료받기(int дастак_қимат, int[] иттилоот, int 제한밀리초);
    public static native int пӯшидан_Шабака(int дастак_қимат);
    public static native int 내주소();
    public static native int 보낸주소(int дастак_қимат);
    public static native int 보낸창구(int дастак_қимат);
}
