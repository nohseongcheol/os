// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 enviar_VALOR 버퍼와 8KiB receber_VALOR Loop_VALOR. 인터럽트 대신 폴링한다. */
public final class rede_driver {
    static int 입출력기준주소 = 0;
    static int receber_cargo = 0, 송신칸 = 0;
    static int[] celular_email = new int[6];
    static int 송신수 = 0, receber_CONT_NÚM = 0, erro_CONT_NÚM = 0;

    static int leitura_Configurações(int celular_número, int posição) {
        celular_VALOR.입출력정수쓰기(0xcf8, 0x80000000 | (celular_número << 11) | posição);
        return celular_VALOR.입출력정수읽기(0xcfc);
    }

    static boolean Preparar() {
        int celular_número = -1;
        for (int ÍNDICE = 0; ÍNDICE < 32; ÍNDICE++) {
            if (leitura_Configurações(ÍNDICE, 0) == 0x813910ec) { celular_número = ÍNDICE; break; }
        }
        if (celular_número < 0) return false;
        int valor_padrão = leitura_Configurações(celular_número, 0x10);
        if ((valor_padrão & 1) == 0 || (valor_padrão & 0xfffffffc) < 0x100 || (valor_padrão & 0xfffffffc) > 65535) return false;
        입출력기준주소 = valor_padrão & 0xfffc;
        int comando = leitura_Configurações(celular_número, 4);
        celular_VALOR.입출력정수쓰기(0xcf8, 0x80000004 | (celular_número << 11));
        celular_VALOR.입출력짧은수쓰기(0xcfc, comando | 5); // I/O 및 bus master Permitir_VALOR, PCI Estado_VALOR 비트는 건드리지 않음
        celular_VALOR.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!redefinir_VALOR()) { 입출력기준주소 = 0; return false; }
        for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) celular_email[ÍNDICE] = celular_VALOR.입출력바이트읽기(입출력기준주소 + ÍNDICE);
        return true;
    }

    static boolean redefinir_VALOR() {
        celular_VALOR.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int iniciar = celular_VALOR.밀리초();
        while ((celular_VALOR.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (celular_VALOR.밀리초() - iniciar > 100) return false;
        receber_cargo = 0; 송신칸 = 0;
        celular_VALOR.입출력정수쓰기(입출력기준주소 + 0x30, celular_VALOR.rede_Memória());
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) celular_VALOR.입출력정수쓰기(입출력기준주소 + 0x20 + ÍNDICE * 4, celular_VALOR.rede_Memória() + 12288);
        celular_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        celular_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        celular_VALOR.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        celular_VALOR.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/difusão_VALOR, wrap 연속 Store_VALOR, 8KiB
        celular_VALOR.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int enviar(int[] dados, int duração_VALOR) {
        if (입출력기준주소 == 0) return -19;
        if (duração_VALOR < 14 || duração_VALOR > 1514) return -90;
        int Status_porta = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int iniciar = celular_VALOR.밀리초();
        while ((celular_VALOR.입출력정수읽기(Status_porta) & 0x2000) == 0)
            if (celular_VALOR.밀리초() - iniciar > 100) return -110;
        int Tamanho = duração_VALOR < 60 ? 60 : duração_VALOR;
        for (int ÍNDICE = 0; ÍNDICE < Tamanho; ÍNDICE++)
            celular_VALOR.gravar_Memória(celular_VALOR.rede_Memória() + 12288 + ÍNDICE, ÍNDICE < duração_VALOR ? dados[ÍNDICE] : 0);
        celular_VALOR.입출력정수쓰기(Status_porta, Tamanho | 0x00080000);
        iniciar = celular_VALOR.밀리초();
        while ((celular_VALOR.입출력정수읽기(Status_porta) & 0xe0008000) == 0)
            if (celular_VALOR.밀리초() - iniciar > 100) return -110;
        if ((celular_VALOR.입출력정수읽기(Status_porta) & 0x8000) == 0) { erro_CONT_NÚM++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return duração_VALOR;
    }

    static int receber(int[] dados) {
        if (입출력기준주소 == 0) return 0;
        if ((celular_VALOR.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            erro_CONT_NÚM++;
            if (!redefinir_VALOR()) 입출력기준주소 = 0;
            return 0;
        }
        if ((celular_VALOR.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int HEAD_VALOR = celular_VALOR.rede_Memória() + receber_cargo;
        int Estado_VALOR = execução_gerente.짧은수(HEAD_VALOR), Tamanho = execução_gerente.짧은수(HEAD_VALOR + 2);
        if (Tamanho == 0xfff0) return 0; // DMA 진행 중
        if (Tamanho < 4 || Tamanho > 1518) {
            erro_CONT_NÚM++;
            if (!redefinir_VALOR()) 입출력기준주소 = 0;
            return 0;
        }
        int duração_VALOR = Tamanho - 4;
        if ((Estado_VALOR & 1) != 0) {
            for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) dados[ÍNDICE] = celular_VALOR.leitura_Memória(HEAD_VALOR + 4 + ÍNDICE);
            receber_CONT_NÚM++;
        } else { duração_VALOR = 0; erro_CONT_NÚM++; }
        receber_cargo = (receber_cargo + Tamanho + 4 + 3) & ~3;
        receber_cargo &= 8191;
        celular_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x38, (receber_cargo - 16) & 65535);
        celular_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return duração_VALOR;
    }
}
