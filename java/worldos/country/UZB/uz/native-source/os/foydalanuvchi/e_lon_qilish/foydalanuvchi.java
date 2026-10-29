// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros foydalanuvchi ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class foydalanuvchi {
    public static native int 파일서술자열기(int[] fayl_kiritish_nom, int ochmoq_Sozlamalar);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int bayt_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Nomi, int[] ma_lumotlar);
    public static native int yozmoq_belgi_VALUE(int 문자);
    public static native int yozmoq_fayl(int[] Nomi, int[] ma_lumotlar, int uzunlik_VALUE);
    public static native int Yozish(String tarkib_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int ochmoq_Tarmoq(int mahalliy_port);
    public static native int yuborish_ma_lumotlar(int deskriptor_VALUE, int manzil, int ko_chirish_joyi_port, int[] ma_lumotlar, int uzunlik_VALUE);
    public static native int 자료받기(int deskriptor_VALUE, int[] ma_lumotlar, int 제한밀리초);
    public static native int yopmoq_Tarmoq(int deskriptor_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int deskriptor_VALUE);
    public static native int 보낸창구(int deskriptor_VALUE);
}
