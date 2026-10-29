// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros umsebenzisi ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class umsebenzisi {
    public static native int 파일서술자열기(int[] ifayela_okufakwayo_igama, int vula_Amasethingi);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int ibhayithi_inani);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Igama, int[] imininingwane);
    public static native int bhala_uhlamvusimo_inani(int 문자);
    public static native int bhala_ifayela(int[] Igama, int[] imininingwane, int ubude_inani);
    public static native int Bhala(String Okuqukethwe_inani);
    public static native int 인수개수();
    public static native String 인수(int thola_inkomba);
    public static native int 실행권한();
    public static native int vula_iNethiwekhi(int endaweni_intuba);
    public static native int Thumela_imininingwane(int isibambo_inani, int ikheli, int isikhumulo_intuba, int[] imininingwane, int ubude_inani);
    public static native int 자료받기(int isibambo_inani, int[] imininingwane, int 제한밀리초);
    public static native int vala_iNethiwekhi(int isibambo_inani);
    public static native int 내주소();
    public static native int 보낸주소(int isibambo_inani);
    public static native int 보낸창구(int isibambo_inani);
}
