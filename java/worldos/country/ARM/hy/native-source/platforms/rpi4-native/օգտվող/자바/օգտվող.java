// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Գործիքներ 전용 SVC Միացնել. 기존 x86 Գործիքներ 원문을 함께 빌드한다. */
public final class օգտվող {
    public static native int 파일서술자열기(int[] Անուն, int Նախընտրանքներ);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int արժեք);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Անուն, int[] տվյալ);
    public static native int գրել_նիշք(int[] Անուն, int[] տվյալ, int տեւողություն_արժեք);
    public static native int Գրել(String Տեքստ);
    public static native int գրել_գրանշան_արժեք(int արժեք);
    public static native int 인수개수();
    public static native String 인수(int դասիչ);
    public static native int 도구번호();
    public static native int 화면연결(int Գործողություն, int դասիչ, int 가, int 나, int 다, int 라);
    public static native int 화면글(int դասիչ, int[] Տեքստ, int տեւողություն_արժեք);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int հոսք_հսկում(int Գործողություն, int 서술자, int արժեք);
    public static native int Կապակցել_հոսք(int 서술자, int հասցե, int միացք_արժեք);
    public static native int բացել_Ցանց(int միացք_արժեք);
    public static native int ուղարկել_Ցանց(int 서술자, int հասցե, int միացք_արժեք, int[] տվյալ, int տեւողություն_արժեք);
    public static native int 통신받기(int 서술자, int[] տվյալ, int տեւողություն_արժեք);
    public static native int Ցանց_միացք(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Ուղղահայաց_դիրք, int 폭, int 높이, int 색);
}
