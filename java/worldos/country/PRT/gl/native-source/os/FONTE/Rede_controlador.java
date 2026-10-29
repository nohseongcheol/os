// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 enviar_VALOR 버퍼와 8KiB 수신 Loop_VALOR. 인터럽트 대신 폴링한다. */
public final class Rede_controlador {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] dispositivo_ENDEREZO = new int[6];
    static int 송신수 = 0, 수신수 = 0, erro_CONTAR = 0;

    static int 설정읽기(int 장치번호, int Posición) {
        dispositivo_VALOR.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Posición);
        return dispositivo_VALOR.입출력정수읽기(0xcfc);
    }

    static boolean 준비() {
        int 장치번호 = -1;
        for (int ÍNDICE = 0; ÍNDICE < 32; ÍNDICE++) {
            if (설정읽기(ÍNDICE, 0) == 0x813910ec) { 장치번호 = ÍNDICE; break; }
        }
        if (장치번호 < 0) return false;
        int valor_predefinido = 설정읽기(장치번호, 0x10);
        if ((valor_predefinido & 1) == 0 || (valor_predefinido & 0xfffffffc) < 0x100 || (valor_predefinido & 0xfffffffc) > 65535) return false;
        입출력기준주소 = valor_predefinido & 0xfffc;
        int Orde = 설정읽기(장치번호, 4);
        dispositivo_VALOR.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        dispositivo_VALOR.입출력짧은수쓰기(0xcfc, Orde | 5); // I/O 및 bus master Permitir_VALOR, PCI Estado_VALOR 비트는 건드리지 않음
        dispositivo_VALOR.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Restablecer_VALOR()) { 입출력기준주소 = 0; return false; }
        for (int ÍNDICE = 0; ÍNDICE < 6; ÍNDICE++) dispositivo_ENDEREZO[ÍNDICE] = dispositivo_VALOR.입출력바이트읽기(입출력기준주소 + ÍNDICE);
        return true;
    }

    static boolean Restablecer_VALOR() {
        dispositivo_VALOR.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Executar_2 = dispositivo_VALOR.밀리초();
        while ((dispositivo_VALOR.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (dispositivo_VALOR.밀리초() - Executar_2 > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        dispositivo_VALOR.입출력정수쓰기(입출력기준주소 + 0x30, dispositivo_VALOR.Rede_Memoria());
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) dispositivo_VALOR.입출력정수쓰기(입출력기준주소 + 0x20 + ÍNDICE * 4, dispositivo_VALOR.Rede_Memoria() + 12288);
        dispositivo_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        dispositivo_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        dispositivo_VALOR.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        dispositivo_VALOR.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/difundir_VALOR, wrap 연속 Store_VALOR, 8KiB
        dispositivo_VALOR.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int enviar(int[] datos, int duración_VALOR) {
        if (입출력기준주소 == 0) return -19;
        if (duración_VALOR < 14 || duración_VALOR > 1514) return -90;
        int estado_porto = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Executar_2 = dispositivo_VALOR.밀리초();
        while ((dispositivo_VALOR.입출력정수읽기(estado_porto) & 0x2000) == 0)
            if (dispositivo_VALOR.밀리초() - Executar_2 > 100) return -110;
        int Tamaño = duración_VALOR < 60 ? 60 : duración_VALOR;
        for (int ÍNDICE = 0; ÍNDICE < Tamaño; ÍNDICE++)
            dispositivo_VALOR.escribir_Memoria(dispositivo_VALOR.Rede_Memoria() + 12288 + ÍNDICE, ÍNDICE < duración_VALOR ? datos[ÍNDICE] : 0);
        dispositivo_VALOR.입출력정수쓰기(estado_porto, Tamaño | 0x00080000);
        Executar_2 = dispositivo_VALOR.밀리초();
        while ((dispositivo_VALOR.입출력정수읽기(estado_porto) & 0xe0008000) == 0)
            if (dispositivo_VALOR.밀리초() - Executar_2 > 100) return -110;
        if ((dispositivo_VALOR.입출력정수읽기(estado_porto) & 0x8000) == 0) { erro_CONTAR++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return duración_VALOR;
    }

    static int 받기(int[] datos) {
        if (입출력기준주소 == 0) return 0;
        if ((dispositivo_VALOR.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            erro_CONTAR++;
            if (!Restablecer_VALOR()) 입출력기준주소 = 0;
            return 0;
        }
        if ((dispositivo_VALOR.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = dispositivo_VALOR.Rede_Memoria() + 수신위치;
        int Estado_VALOR = 실행관리.짧은수(머리), Tamaño = 실행관리.짧은수(머리 + 2);
        if (Tamaño == 0xfff0) return 0; // DMA 진행 중
        if (Tamaño < 4 || Tamaño > 1518) {
            erro_CONTAR++;
            if (!Restablecer_VALOR()) 입출력기준주소 = 0;
            return 0;
        }
        int duración_VALOR = Tamaño - 4;
        if ((Estado_VALOR & 1) != 0) {
            for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) datos[ÍNDICE] = dispositivo_VALOR.기억읽기(머리 + 4 + ÍNDICE);
            수신수++;
        } else { duración_VALOR = 0; erro_CONTAR++; }
        수신위치 = (수신위치 + Tamaño + 4 + 3) & ~3;
        수신위치 &= 8191;
        dispositivo_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        dispositivo_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return duración_VALOR;
    }
}
