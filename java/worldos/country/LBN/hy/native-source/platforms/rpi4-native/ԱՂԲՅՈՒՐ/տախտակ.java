// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 մեքենա 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class տախտակ {
    public static native int 표시화소읽기(int 가로, int Ուղղահայաց_դիրք);
    public static native void գրել_ցուցադրել_փիքսել(int 가로, int Ուղղահայաց_դիրք, int 색);
    public static native int հետեւում(int 종류, int Գործողություն);
    public static native void վերջացնել_հեռակա_հրաման(int վիճակ_արժեք);
    public static native void 원격대기(int վիճակ_արժեք);
    public static native void 직렬쓰기(int արժեք);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int պրոցեսոր_թույլտվություն_մակարդակ();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Ուղղահայաց_դիրք, int 색);
    public static native void կասեցնել_պրոցեսոր();
    public static native int Կերտի_ր_խնդիր(int դասիչ);
    public static native int խնդիր_վիճակ(int դասիչ);
    public static native void Կանգառ(int վիճակ_արժեք);
    public static native int 씨플러스시험();
    public static native int աշխատեցնել_օգտվող_ծրագիր(int դասիչ);
    public static native int կտրոն_օգտվող_ծրագիր();
    public static native int 인수준비(int 개수);
    public static native int կատարել_օգտվող_նիշք();
    public static native int 리눅스파일실행();
    public static native int արգումենտ_բայթ(int դասիչ, int Դիրք, int արժեք);
    public static native int Տերմինալ(int Գործողություն);
    public static native int հսկում_օգտվող_ծրագիր(int Գործողություն);
    public static native void 입출력전환(int Գործողություն);
    public static native int նիշք_փոխանցել_ծառայություն(int Գործողություն);
    public static native int Ցանց_վիճակ(int մուտքագրում_արժեք, int դասիչ);
    public static native int Ցանց_Կարգավորումներ(int Գործողություն, int հասցե, int դիմակ_արժեք, int անցուղի_արժեք);
    public static native int 응답보내기(int հասցե, int կարգ_արժեք);
    public static native int 응답읽기(int մուտքագրում_արժեք);
    public static native int հարցում_համակարգ(int մուտքագրում_արժեք, int դասիչ);
    public static native void 전원끄기();
}
