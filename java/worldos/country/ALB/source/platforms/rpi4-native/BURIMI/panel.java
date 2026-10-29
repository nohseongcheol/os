// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 makinë 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class panel {
    public static native int 표시화소읽기(int 가로, int Vertikal_pozicioni);
    public static native void shkruaj_afishim_pikëz(int 가로, int Vertikal_pozicioni, int 색);
    public static native int ndjekja_paralele(int 종류, int Veprim);
    public static native void mbaroj_në_largësi_komandë(int status_VALUE);
    public static native void në_largësi_Prit(int status_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_leje_nivel();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int Vertikal_pozicioni, int 색);
    public static native void YIELD_CPU();
    public static native int Krijo_detyrë(int INDEX);
    public static native int detyrë_status(int INDEX);
    public static native void Ndalo(int status_VALUE);
    public static native int 씨플러스시험();
    public static native int varg_përdorues_program(int INDEX);
    public static native int çek_përdorues_program();
    public static native int 인수준비(int njësi_COUNT);
    public static native int zbatoj_përdorues_skedar();
    public static native int 리눅스파일실행();
    public static native int argument_bajt(int INDEX, int Pozicioni, int VALUE);
    public static native int Terminali(int Veprim);
    public static native int kontroll_përdorues_program(int Veprim);
    public static native void 입출력전환(int Veprim);
    public static native int skedar_transferim_shërbim(int Veprim);
    public static native int rrjet_status(int futje_VALUE, int INDEX);
    public static native int rrjet_cilësimet(int Veprim, int email, int maskë_VALUE, int portëkalimi_VALUE);
    public static native int dërgoj_përgjigje(int email, int renditja_VALUE);
    public static native int 응답읽기(int futje_VALUE);
    public static native int pyetja_sistem(int futje_VALUE, int INDEX);
    public static native void 전원끄기();
}
