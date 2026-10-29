// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Куралдар 전용 SVC Туташуу. 기존 x86 Куралдар 원문을 함께 빌드한다. */
public final class колдонуучу {
    public static native int 파일서술자열기(int[] Аты, int Орнотуулар);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int маани);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Аты, int[] берилмелер);
    public static native int жазуу_файл(int[] Аты, int[] берилмелер, int узундук_маани);
    public static native int Жазуу(String Текст);
    public static native int жазуу_символ_маани(int маани);
    public static native int 인수개수();
    public static native String 인수(int индекс);
    public static native int 도구번호();
    public static native int 화면연결(int Аракети, int индекс, int 가, int 나, int 다, int 라);
    public static native int 화면글(int индекс, int[] Текст, int узундук_маани);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int агым_башкаруу(int Аракети, int 서술자, int маани);
    public static native int ТУТАШУУ_агым(int 서술자, int дарек, int порт_маани);
    public static native int ачуу_Желе(int порт_маани);
    public static native int жөнөтүү_Желе(int 서술자, int дарек, int порт_маани, int[] берилмелер, int узундук_маани);
    public static native int 통신받기(int 서술자, int[] берилмелер, int узундук_маани);
    public static native int Желе_порт(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
