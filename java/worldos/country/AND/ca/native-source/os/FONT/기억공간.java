// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Mida 작업 secció_VALOR assignar_Emmagatzematge/tornar_les_tasques_mesura. 일반 물리 pàgina_VALOR 관리자는 아니다. */
public final class 기억공간 {
    static int[] secció_VALOR = new int[8192];
    static int[] ús_VALOR = new int[8];

    static int 정수읽기(int Adreça) {
        return dispositiu_VALOR.tancar_Memòria(Adreça) | (dispositiu_VALOR.tancar_Memòria(Adreça + 1) << 8)
            | (dispositiu_VALOR.tancar_Memòria(Adreça + 2) << 16) | (dispositiu_VALOR.tancar_Memòria(Adreça + 3) << 24);
    }

    static int MAJUSC_Memòria_canviar_la_mida() {
        int msinfo32_exe = dispositiu_VALOR.부팅정보();
        if (dispositiu_VALOR.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (정수읽기(msinfo32_exe) & 1) == 0) return -1;
        return 정수읽기(msinfo32_exe + 8);
    }

    static int assignar_Emmagatzematge() {
        for (int INDEX = 0; INDEX < ús_VALOR.length; INDEX++) {
            if (ús_VALOR[INDEX] == 0) {
                ús_VALOR[INDEX] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) secció_VALOR[INDEX * 1024 + 칸] = 0;
                return INDEX;
            }
        }
        return -1;
    }

    static boolean tornar_les_tasques_mesura(int INDEX) {
        if (INDEX < 0 || INDEX >= ús_VALOR.length || ús_VALOR[INDEX] == 0) return false;
        ús_VALOR[INDEX] = 0;
        return true;
    }

    static int 사용개수() {
        int element_COMPT = 0;
        for (int INDEX = 0; INDEX < ús_VALOR.length; INDEX++) element_COMPT += ús_VALOR[INDEX];
        return element_COMPT;
    }
}
