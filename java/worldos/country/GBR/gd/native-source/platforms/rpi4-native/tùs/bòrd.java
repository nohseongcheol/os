// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 inneal 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class bòrd {
    public static native int 표시화소읽기(int 가로, int inghearach_suidhich);
    public static native void sgrìobh_taisbean_pel(int 가로, int inghearach_suidhich, int 색);
    public static native int co_sheisean(int 종류, int Gnìomh);
    public static native void crìochnaich_cian_àithne(int cor_VALUE);
    public static native void cian_fuirich(int cor_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int inghearach_suidhich, int 색);
    public static native void YIELD_CPU();
    public static native int Create_saothair(int INDEX);
    public static native int saothair_cor(int INDEX);
    public static native void Stad(int cor_VALUE);
    public static native int 씨플러스시험();
    public static native int ruith_cleachdaiche_ap(int INDEX);
    public static native int seic_cleachdaiche_ap();
    public static native int 인수준비(int nì_COUNT);
    public static native int gnìomhaich_cleachdaiche_faidhle();
    public static native int 리눅스파일실행();
    public static native int argamaid_baidht(int INDEX, int suidhich, int VALUE);
    public static native int tèirmineal(int Gnìomh);
    public static native int smachd_cleachdaiche_ap(int Gnìomh);
    public static native void 입출력전환(int Gnìomh);
    public static native int faidhle_tar_chur_seirbheis(int Gnìomh);
    public static native int lìonra_cor(int cur_a_steach_VALUE, int INDEX);
    public static native int lìonra_roghainnean(int Gnìomh, int ADDRESS, int 가림, int 관문);
    public static native int 응답보내기(int ADDRESS, int òrdugh_VALUE);
    public static native int 응답읽기(int cur_a_steach_VALUE);
    public static native int ceist_siostam(int cur_a_steach_VALUE, int INDEX);
    public static native void 전원끄기();
}
