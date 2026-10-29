// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros istifadəçi ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class istifadəçi {
    public static native int 파일서술자열기(int[] fayl_daxiletmə_ad, int açmaq_Parametrlər);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bayt_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Ad, int[] verilənlər);
    public static native int yazmaq_simvol_VALUE(int 문자);
    public static native int yazmaq_fayl(int[] Ad, int[] verilənlər, int uzunluq_VALUE);
    public static native int Yazma(String Məzmun_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int açmaq_Şəbəkə(int lokal_port);
    public static native int göndərmək_verilənlər(int tutacaq_VALUE, int ünvan, int təyinat_port, int[] verilənlər, int uzunluq_VALUE);
    public static native int 자료받기(int tutacaq_VALUE, int[] verilənlər, int 제한밀리초);
    public static native int bağlamaq_Şəbəkə(int tutacaq_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int tutacaq_VALUE);
    public static native int 보낸창구(int tutacaq_VALUE);
}
