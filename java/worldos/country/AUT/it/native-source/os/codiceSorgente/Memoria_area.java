// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** avvio_macchina msinfo32_exe 조회와 4KiB 고정 Dimensione 작업 sezione_VALORE allocare_Memoria/Reso_KR. 일반 물리 pagina_VALORE 관리자는 아니다. */
public final class Memoria_area {
    static int[] sezione_VALORE = new int[8192];
    static int[] usare_VALORE = new int[8];

    static int analizzare_intero(int e_mail) {
        return cellulare_VALORE.기억읽기(e_mail) | (cellulare_VALORE.기억읽기(e_mail + 1) << 8)
            | (cellulare_VALORE.기억읽기(e_mail + 2) << 16) | (cellulare_VALORE.기억읽기(e_mail + 3) << 24);
    }

    static int MAIUSC_Memoria_ridimensionare() {
        int msinfo32_exe = cellulare_VALORE.부팅정보();
        if (cellulare_VALORE.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (analizzare_intero(msinfo32_exe) & 1) == 0) return -1;
        return analizzare_intero(msinfo32_exe + 8);
    }

    static int allocare_Memoria() {
        for (int INDICE = 0; INDICE < usare_VALORE.length; INDICE++) {
            if (usare_VALORE[INDICE] == 0) {
                usare_VALORE[INDICE] = 1;
                for (int slot_voce = 0; slot_voce < 1024; slot_voce++) sezione_VALORE[INDICE * 1024 + slot_voce] = 0;
                return INDICE;
            }
        }
        return -1;
    }

    static boolean Reso_KR(int INDICE) {
        if (INDICE < 0 || INDICE >= usare_VALORE.length || usare_VALORE[INDICE] == 0) return false;
        usare_VALORE[INDICE] = 0;
        return true;
    }

    static int 사용개수() {
        int articolo_CONTA_NUMERI = 0;
        for (int INDICE = 0; INDICE < usare_VALORE.length; INDICE++) articolo_CONTA_NUMERI += usare_VALORE[INDICE];
        return articolo_CONTA_NUMERI;
    }
}
