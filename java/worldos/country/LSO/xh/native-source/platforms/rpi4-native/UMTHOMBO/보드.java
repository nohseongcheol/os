// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 umatshini 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void bhala_bonisa_i_pel(int 가로, int 세로, int 색);
    public static native int ukusitha(int 종류, int Intshukumo);
    public static native void phela_kude_umyalelo(int imo_ixabiso);
    public static native void 원격대기(int imo_ixabiso);
    public static native void 직렬쓰기(int ixabiso);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int i_CPU_imvume_inqanaba();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void misa_okwexeshana_i_CPU();
    public static native int yila_umsebenzi(int indeksa);
    public static native int umsebenzi_imo(int indeksa);
    public static native void Yima(int imo_ixabiso);
    public static native int 씨플러스시험();
    public static native int i_run_umsebenzisi_inkqubo(int indeksa);
    public static native int jonga_umsebenzisi_inkqubo();
    public static native int 인수준비(int 개수);
    public static native int ukwenza_umsebenzisi_ifayile();
    public static native int 리눅스파일실행();
    public static native int isiniki_myalelo_ibhayithi(int indeksa, int 위치, int ixabiso);
    public static native int i_Terminal(int Intshukumo);
    public static native int isilawuli_umsebenzisi_inkqubo(int Intshukumo);
    public static native void 입출력전환(int Intshukumo);
    public static native int ifayile_gqithisela_isevisi(int Intshukumo);
    public static native int Inethiwekhi_imo(int ufako_nkcukacha_ixabiso, int indeksa);
    public static native int Inethiwekhi_Iisetingi(int Intshukumo, int idilesi, int imaskhi_ixabiso, int isango_lekhompyutha_ixabiso);
    public static native int 응답보내기(int idilesi, int ulandelelwano_ixabiso);
    public static native int 응답읽기(int ufako_nkcukacha_ixabiso);
    public static native int umbuzo_inkqubo(int ufako_nkcukacha_ixabiso, int indeksa);
    public static native void 전원끄기();
}
