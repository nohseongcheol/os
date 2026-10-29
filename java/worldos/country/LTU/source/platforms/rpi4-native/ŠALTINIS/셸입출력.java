// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], išeiga_duomenys = new int[16384];
    static int 입력길이, 입력위치, 출력길이, įvesties_failas = -1, išvesties_failas = -1;
    static boolean 파이프입력, vertikalus_brūkšnys_išeiga;
    static int triktis_VALUE;
    static boolean 대화허용 = true;
    public static int 대화가능() { return 대화허용 && įvesties_failas < 3 && išvesties_failas < 3 && !파이프입력 && !vertikalus_brūkšnys_išeiga ? 1 : 0; }
    public static int Išvestis(int kanalas_VALUE, int VALUE) {
        if (kanalas_VALUE != 1) return 0;
        if (išvesties_failas >= 3) { int 처리값 = atmintis_Failai.Rašymas(išvesties_failas, VALUE); if (처리값 < 0) triktis_VALUE = 처리값; return 1; }
        if (!vertikalus_brūkšnys_išeiga) return 0;
        if (출력길이 == išeiga_duomenys.length) triktis_VALUE = -28;
        else išeiga_duomenys[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (įvesties_failas >= 3) { int 처리값 = atmintis_Failai.Skaitymas(įvesties_failas); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Pirmyn_VALUE
    }
    static void Paleisti(boolean eilučių_intervalas_vertikalus_brūkšnys, boolean 뒤파이프) {
        파이프입력 = eilučių_intervalas_vertikalus_brūkšnys; vertikalus_brūkšnys_išeiga = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; įvesties_failas = -1; išvesties_failas = -1; triktis_VALUE = 0;
    }
    static void 끝() {
        Lenta.입출력전환(0);
        if (įvesties_failas >= 3) atmintis_Failai.Užverti(įvesties_failas);
        if (išvesties_failas >= 3) atmintis_Failai.Užverti(išvesties_failas);
        if (vertikalus_brūkšnys_išeiga) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = išeiga_duomenys[Loop_INDEX]; }
        įvesties_failas = -1; išvesties_failas = -1; 파이프입력 = false; vertikalus_brūkšnys_išeiga = false;
    }
}
