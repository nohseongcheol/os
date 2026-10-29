// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 msinfo32_exe 조회와 4KiB 고정 Tamaño 작업 sección_VALOR atribuír_Almacenamento/devolver_medida. 일반 물리 páxina_VALOR 관리자는 아니다. */
public final class 기억공간 {
    static int[] sección_VALOR = new int[8192];
    static int[] 사용 = new int[8];

    static int analizar_número_enteiro(int ENDEREZO) {
        return dispositivo_VALOR.기억읽기(ENDEREZO) | (dispositivo_VALOR.기억읽기(ENDEREZO + 1) << 8)
            | (dispositivo_VALOR.기억읽기(ENDEREZO + 2) << 16) | (dispositivo_VALOR.기억읽기(ENDEREZO + 3) << 24);
    }

    static int 위쪽기억크기() {
        int msinfo32_exe = dispositivo_VALOR.부팅정보();
        if (dispositivo_VALOR.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (analizar_número_enteiro(msinfo32_exe) & 1) == 0) return -1;
        return analizar_número_enteiro(msinfo32_exe + 8);
    }

    static int atribuír_Almacenamento() {
        for (int ÍNDICE = 0; ÍNDICE < 사용.length; ÍNDICE++) {
            if (사용[ÍNDICE] == 0) {
                사용[ÍNDICE] = 1;
                for (int 칸 = 0; 칸 < 1024; 칸++) sección_VALOR[ÍNDICE * 1024 + 칸] = 0;
                return ÍNDICE;
            }
        }
        return -1;
    }

    static boolean devolver_medida(int ÍNDICE) {
        if (ÍNDICE < 0 || ÍNDICE >= 사용.length || 사용[ÍNDICE] == 0) return false;
        사용[ÍNDICE] = 0;
        return true;
    }

    static int 사용개수() {
        int elemento_CONTAR = 0;
        for (int ÍNDICE = 0; ÍNDICE < 사용.length; ÍNDICE++) elemento_CONTAR += 사용[ÍNDICE];
        return elemento_CONTAR;
    }
}
