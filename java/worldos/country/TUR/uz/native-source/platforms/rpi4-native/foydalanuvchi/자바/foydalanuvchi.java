// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Vositalar 전용 SVC Ulanish. 기존 x86 Vositalar 원문을 함께 빌드한다. */
public final class foydalanuvchi {
    public static native int 파일서술자열기(int[] Nomi, int Moslamalar);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Nomi, int[] ma_lumotlar);
    public static native int yozmoq_fayl(int[] Nomi, int[] ma_lumotlar, int uzunlik_VALUE);
    public static native int Yozish(String Matn);
    public static native int yozmoq_belgi_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Amal, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Matn, int uzunlik_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int oqim_boshqaruv(int Amal, int 서술자, int VALUE);
    public static native int ulash_oqim(int 서술자, int manzil, int port_VALUE);
    public static native int ochmoq_Tarmoq(int port_VALUE);
    public static native int yuborish_Tarmoq(int 서술자, int manzil, int port_VALUE, int[] ma_lumotlar, int uzunlik_VALUE);
    public static native int 통신받기(int 서술자, int[] ma_lumotlar, int uzunlik_VALUE);
    public static native int Tarmoq_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Vertikal_holat, int 폭, int 높이, int 색);
}
