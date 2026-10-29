// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros колдонуучу ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class колдонуучу {
    public static native int 파일서술자열기(int[] файл_киргизме_жазуу_аты, int ачуу_Орнотуулар);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int байт_маани);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Аты, int[] берилмелер);
    public static native int жазуу_символ_маани(int 문자);
    public static native int жазуу_файл(int[] Аты, int[] берилмелер, int узундук_маани);
    public static native int Жазуу(String Мазмун_маани);
    public static native int 인수개수();
    public static native String 인수(int индекс);
    public static native int 실행권한();
    public static native int ачуу_Желе(int локалдык_порт);
    public static native int жөнөтүү_берилмелер(int тутка_маани, int дарек, int көздөө_жайы_порт, int[] берилмелер, int узундук_маани);
    public static native int 자료받기(int тутка_маани, int[] берилмелер, int 제한밀리초);
    public static native int жабуу_Желе(int тутка_маани);
    public static native int 내주소();
    public static native int 보낸주소(int тутка_маани);
    public static native int 보낸창구(int тутка_маани);
}
