// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 mašina 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Lenta {
    public static native int 표시화소읽기(int 가로, int segmentas_padėtis);
    public static native void rašymas_rodyti_pikselis(int 가로, int segmentas_padėtis, int 색);
    public static native int stebėjimas(int 종류, int Veiksmas);
    public static native void baigti_pokalbį_nuotolinis_komanda(int Būsena_VALUE);
    public static native void nuotolinis_Palauk(int Būsena_VALUE);
    public static native void 직렬쓰기(int VALUE);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_teisė_lygis();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int segmentas_padėtis, int 색);
    public static native void YIELD_CPU();
    public static native int kurti_užduotis(int INDEX);
    public static native int užduotis_Būsena(int INDEX);
    public static native void Sustabdyti(int Būsena_VALUE);
    public static native int 씨플러스시험();
    public static native int vykdyti_naudotojas_programa(int INDEX);
    public static native int čekis_naudotojas_programa();
    public static native int 인수준비(int prekė_COUNT);
    public static native int Vykdyti_naudotojas_Failas();
    public static native int 리눅스파일실행();
    public static native int argumentas_baitas(int INDEX, int Pozicija, int VALUE);
    public static native int Terminalas(int Veiksmas);
    public static native int valdymas_naudotojas_programa(int Veiksmas);
    public static native void 입출력전환(int Veiksmas);
    public static native int failo_perdavimas_tarnyba(int Veiksmas);
    public static native int tinklas_būsena(int įrašas_VALUE, int INDEX);
    public static native int tinklas_Parametrai(int Veiksmas, int ADDRESS, int šablonas_VALUE, int šliuzas_VALUE);
    public static native int siųsti_atsakas(int ADDRESS, int tvarka_VALUE);
    public static native int 응답읽기(int įrašas_VALUE);
    public static native int užklausa_sistema(int įrašas_VALUE, int INDEX);
    public static native void 전원끄기();
}
