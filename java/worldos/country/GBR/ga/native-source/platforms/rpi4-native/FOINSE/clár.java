// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 meaisín 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class clár {
    public static native int 표시화소읽기(int 가로, int Ingearach_suíomh);
    public static native void scríobh_taispeáin_picteilín(int 가로, int Ingearach_suíomh, int 색);
    public static native int scáthú(int 종류, int Gníomh);
    public static native void cuir_deireadh_le_cianda_ordú(int staid_VALUE);
    public static native void 원격대기(int staid_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_cead_leibhéal();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Ingearach_suíomh, int 색);
    public static native void YIELD_CPU();
    public static native int Create_tasc(int INDEX);
    public static native int tasc_staid(int INDEX);
    public static native void Stad(int staid_VALUE);
    public static native int 씨플러스시험();
    public static native int rith_úsáideoir_clár(int INDEX);
    public static native int seic_úsáideoir_clár();
    public static native int 인수준비(int mír_COUNT);
    public static native int Rith_úsáideoir_comhad();
    public static native int 리눅스파일실행();
    public static native int argóint_beart(int INDEX, int suíomh, int VALUE);
    public static native int Teirminéal(int Gníomh);
    public static native int rialú_úsáideoir_clár(int Gníomh);
    public static native void 입출력전환(int Gníomh);
    public static native int comhad_traschur_seirbhís(int Gníomh);
    public static native int Líonra_staid(int iontráil_VALUE, int INDEX);
    public static native int Líonra_Socruithe(int Gníomh, int ADDRESS, int masc_VALUE, int geata_VALUE);
    public static native int 응답보내기(int ADDRESS, int ord_VALUE);
    public static native int 응답읽기(int iontráil_VALUE);
    public static native int iarratas_córas(int iontráil_VALUE, int INDEX);
    public static native void 전원끄기();
}
