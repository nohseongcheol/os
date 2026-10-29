// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Ibikoresho 전용 SVC Guhuza. 기존 x86 Ibikoresho 원문을 함께 빌드한다. */
public final class ukoresha {
    public static native int 파일서술자열기(int[] Izina, int Amagenamiterere);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int agaciro);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Izina, int[] amakurushingiro);
    public static native int kwandika_dosiye(int[] Izina, int[] amakurushingiro, int uburebure_agaciro);
    public static native int kwandika(String Umwandiko);
    public static native int kwandika_inyuguti_agaciro(int agaciro);
    public static native int 인수개수();
    public static native String 인수(int umugerekashakiro);
    public static native int 도구번호();
    public static native int 화면연결(int Igikorwa, int umugerekashakiro, int 가, int 나, int 다, int 라);
    public static native int 화면글(int umugerekashakiro, int[] Umwandiko, int uburebure_agaciro);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_icunga(int Igikorwa, int 서술자, int agaciro);
    public static native int Guhuza_Stream(int 서술자, int aderesi, int poti_agaciro);
    public static native int kurema_Urusobemiyoboro(int poti_agaciro);
    public static native int kohereza_Urusobemiyoboro(int 서술자, int aderesi, int poti_agaciro, int[] amakurushingiro, int uburebure_agaciro);
    public static native int 통신받기(int 서술자, int[] amakurushingiro, int uburebure_agaciro);
    public static native int Urusobemiyoboro_poti(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
