// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 kompjuter 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class bord {
    public static native int 표시화소읽기(int 가로, int Vertikali_pożizzjoni);
    public static native void kiteb_wera_pel(int 가로, int Vertikali_pożizzjoni, int 색);
    public static native int insegwiment(int 종류, int azzjoni);
    public static native void ttermina_mill_bogħod_kmand(int stat_VALUE);
    public static native void 원격대기(int stat_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_permess_livell();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Vertikali_pożizzjoni, int 색);
    public static native void YIELD_CPU();
    public static native int ħalaq_attività(int INDEX);
    public static native int attività_stat(int INDEX);
    public static native void waqqaf(int stat_VALUE);
    public static native int 씨플러스시험();
    public static native int serje_utent_programm(int INDEX);
    public static native int ċekk_utent_programm();
    public static native int 인수준비(int element_COUNT);
    public static native int eżegwixxa_utent_fajl();
    public static native int 리눅스파일실행();
    public static native int argument_byte(int INDEX, int pożizzjoni, int VALUE);
    public static native int Terminal(int azzjoni);
    public static native int kontroll_utent_programm(int azzjoni);
    public static native void 입출력전환(int azzjoni);
    public static native int fajl_trasferiment_servizz(int azzjoni);
    public static native int netwerk_stat(int entrata_VALUE, int INDEX);
    public static native int netwerk_Settings(int azzjoni, int ADDRESS, int maskra_VALUE, int gateway_VALUE);
    public static native int 응답보내기(int ADDRESS, int ordni_VALUE);
    public static native int 응답읽기(int entrata_VALUE);
    public static native int query_sistema(int entrata_VALUE, int INDEX);
    public static native void 전원끄기();
}
