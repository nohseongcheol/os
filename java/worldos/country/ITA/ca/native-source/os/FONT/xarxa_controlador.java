// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 enviar_VALOR 버퍼와 8KiB rebre_VALOR Loop_VALOR. 인터럽트 대신 폴링한다. */
public final class xarxa_controlador {
    static int 입출력기준주소 = 0;
    static int rebre_càrrec = 0, 송신칸 = 0;
    static int[] dispositiu_ADREÇA = new int[6];
    static int 송신수 = 0, rebre_COMPT = 0, error_COMPT = 0;

    static int tancar_Configuració(int 장치번호, int Posició) {
        dispositiu_VALOR.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Posició);
        return dispositiu_VALOR.입출력정수읽기(0xcfc);
    }

    static boolean Prepara() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (tancar_Configuració(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int valor_per_defecte = tancar_Configuració(장치번호, 0x10);
        if ((valor_per_defecte & 1) == 0 || (valor_per_defecte & 0xfffffffc) < 0x100 || (valor_per_defecte & 0xfffffffc) > 65535) return false;
        입출력기준주소 = valor_per_defecte & 0xfffc;
        int Ordre = tancar_Configuració(장치번호, 4);
        dispositiu_VALOR.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        dispositiu_VALOR.입출력짧은수쓰기(0xcfc, Ordre | 5); // I/O 및 bus master Permet_VALOR, PCI Estat_VALOR 비트는 건드리지 않음
        dispositiu_VALOR.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!restablir_VALOR()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) dispositiu_ADREÇA[INDEX] = dispositiu_VALOR.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean restablir_VALOR() {
        dispositiu_VALOR.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Executa_2 = dispositiu_VALOR.밀리초();
        while ((dispositiu_VALOR.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (dispositiu_VALOR.밀리초() - Executa_2 > 100) return false;
        rebre_càrrec = 0; 송신칸 = 0;
        dispositiu_VALOR.입출력정수쓰기(입출력기준주소 + 0x30, dispositiu_VALOR.xarxa_Memòria());
        for (int INDEX = 0; INDEX < 4; INDEX++) dispositiu_VALOR.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, dispositiu_VALOR.xarxa_Memòria() + 12288);
        dispositiu_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        dispositiu_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        dispositiu_VALOR.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        dispositiu_VALOR.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/de_difusió_VALOR, wrap 연속 Store_VALOR, 8KiB
        dispositiu_VALOR.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int enviar(int[] dades, int durada_VALOR) {
        if (입출력기준주소 == 0) return -19;
        if (durada_VALOR < 14 || durada_VALOR > 1514) return -90;
        int estat_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Executa_2 = dispositiu_VALOR.밀리초();
        while ((dispositiu_VALOR.입출력정수읽기(estat_port) & 0x2000) == 0)
            if (dispositiu_VALOR.밀리초() - Executa_2 > 100) return -110;
        int Mida = durada_VALOR < 60 ? 60 : durada_VALOR;
        for (int INDEX = 0; INDEX < Mida; INDEX++)
            dispositiu_VALOR.escriure_Memòria(dispositiu_VALOR.xarxa_Memòria() + 12288 + INDEX, INDEX < durada_VALOR ? dades[INDEX] : 0);
        dispositiu_VALOR.입출력정수쓰기(estat_port, Mida | 0x00080000);
        Executa_2 = dispositiu_VALOR.밀리초();
        while ((dispositiu_VALOR.입출력정수읽기(estat_port) & 0xe0008000) == 0)
            if (dispositiu_VALOR.밀리초() - Executa_2 > 100) return -110;
        if ((dispositiu_VALOR.입출력정수읽기(estat_port) & 0x8000) == 0) { error_COMPT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return durada_VALOR;
    }

    static int rebre(int[] dades) {
        if (입출력기준주소 == 0) return 0;
        if ((dispositiu_VALOR.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            error_COMPT++;
            if (!restablir_VALOR()) 입출력기준주소 = 0;
            return 0;
        }
        if ((dispositiu_VALOR.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = dispositiu_VALOR.xarxa_Memòria() + rebre_càrrec;
        int Estat_VALOR = 실행관리.짧은수(머리), Mida = 실행관리.짧은수(머리 + 2);
        if (Mida == 0xfff0) return 0; // DMA 진행 중
        if (Mida < 4 || Mida > 1518) {
            error_COMPT++;
            if (!restablir_VALOR()) 입출력기준주소 = 0;
            return 0;
        }
        int durada_VALOR = Mida - 4;
        if ((Estat_VALOR & 1) != 0) {
            for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) dades[INDEX] = dispositiu_VALOR.tancar_Memòria(머리 + 4 + INDEX);
            rebre_COMPT++;
        } else { durada_VALOR = 0; error_COMPT++; }
        rebre_càrrec = (rebre_càrrec + Mida + 4 + 3) & ~3;
        rebre_càrrec &= 8191;
        dispositiu_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x38, (rebre_càrrec - 16) & 65535);
        dispositiu_VALOR.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return durada_VALOR;
    }
}
