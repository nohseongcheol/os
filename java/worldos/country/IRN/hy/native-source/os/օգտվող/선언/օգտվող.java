// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros օգտվող ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class օգտվող {
    public static native int 파일서술자열기(int[] նիշք_մուտքագրում_անուն, int բացել_Կարգավորումներ);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int բայթ_արժեք);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Անուն, int[] տվյալ);
    public static native int գրել_գրանշան_արժեք(int 문자);
    public static native int գրել_նիշք(int[] Անուն, int[] տվյալ, int տեւողություն_արժեք);
    public static native int Գրել(String Բովանդակություն_արժեք);
    public static native int 인수개수();
    public static native String 인수(int դասիչ);
    public static native int 실행권한();
    public static native int բացել_Ցանց(int տեղային_միացք);
    public static native int ուղարկել_տվյալ(int բռնակ_արժեք, int հասցե, int նպատակակետ_միացք, int[] տվյալ, int տեւողություն_արժեք);
    public static native int 자료받기(int բռնակ_արժեք, int[] տվյալ, int 제한밀리초);
    public static native int փակել_Ցանց(int բռնակ_արժեք);
    public static native int 내주소();
    public static native int 보낸주소(int բռնակ_արժեք);
    public static native int 보낸창구(int բռնակ_արժեք);
}
