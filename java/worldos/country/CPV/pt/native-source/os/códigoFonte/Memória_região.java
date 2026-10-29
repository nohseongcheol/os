// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** arranque_da_máquina msinfo32_exe 조회와 4KiB 고정 Tamanho 작업 seção_VALOR alocar_Armazenamento/devolver_RC. 일반 물리 página_VALOR 관리자는 아니다. */
public final class Memória_região {
    static int[] seção_VALOR = new int[8192];
    static int[] uso_VALOR = new int[8];

    static int analisar_inteiro(int Endereço) {
        return celular_VALOR.leitura_Memória(Endereço) | (celular_VALOR.leitura_Memória(Endereço + 1) << 8)
            | (celular_VALOR.leitura_Memória(Endereço + 2) << 16) | (celular_VALOR.leitura_Memória(Endereço + 3) << 24);
    }

    static int MAIÚSCULA_Memória_dimensionar() {
        int msinfo32_exe = celular_VALOR.부팅정보();
        if (celular_VALOR.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (analisar_inteiro(msinfo32_exe) & 1) == 0) return -1;
        return analisar_inteiro(msinfo32_exe + 8);
    }

    static int alocar_Armazenamento() {
        for (int ÍNDICE = 0; ÍNDICE < uso_VALOR.length; ÍNDICE++) {
            if (uso_VALOR[ÍNDICE] == 0) {
                uso_VALOR[ÍNDICE] = 1;
                for (int slot_entrada = 0; slot_entrada < 1024; slot_entrada++) seção_VALOR[ÍNDICE * 1024 + slot_entrada] = 0;
                return ÍNDICE;
            }
        }
        return -1;
    }

    static boolean devolver_RC(int ÍNDICE) {
        if (ÍNDICE < 0 || ÍNDICE >= uso_VALOR.length || uso_VALOR[ÍNDICE] == 0) return false;
        uso_VALOR[ÍNDICE] = 0;
        return true;
    }

    static int 사용개수() {
        int item_CONT_NÚM = 0;
        for (int ÍNDICE = 0; ÍNDICE < uso_VALOR.length; ÍNDICE++) item_CONT_NÚM += uso_VALOR[ÍNDICE];
        return item_CONT_NÚM;
    }
}
