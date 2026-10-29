// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros umsebenzisi ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class umsebenzisi {
    public static native int 파일서술자열기(int[] ifayile_ufako_nkcukacha_igama, int vula_Iisetingi);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int ibhayithi_ixabiso);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Igama, int[] iingcombolo);
    public static native int bhala_ikharakhtha_ixabiso(int 문자);
    public static native int bhala_ifayile(int[] Igama, int[] iingcombolo, int ubude_ixabiso);
    public static native int Bhala(String Isiqulatho_ixabiso);
    public static native int 인수개수();
    public static native String 인수(int indeksa);
    public static native int 실행권한();
    public static native int vula_Inethiwekhi(int eyale_ndawo_iphothi);
    public static native int thumela_iingcombolo(int isibambi_ixabiso, int idilesi, int indawo_ekuyiwa_kuyo_iphothi, int[] iingcombolo, int ubude_ixabiso);
    public static native int 자료받기(int isibambi_ixabiso, int[] iingcombolo, int 제한밀리초);
    public static native int vala_Inethiwekhi(int isibambi_ixabiso);
    public static native int 내주소();
    public static native int 보낸주소(int isibambi_ixabiso);
    public static native int 보낸창구(int isibambi_ixabiso);
}
