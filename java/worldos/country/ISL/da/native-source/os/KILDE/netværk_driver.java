// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 maile_VÆRDI 버퍼와 8KiB modtage_VÆRDI Loop_VÆRDI. 인터럽트 대신 폴링한다. */
public final class netværk_driver {
    static int 입출력기준주소 = 0;
    static int modtage_placere = 0, 송신칸 = 0;
    static int[] enhed_mail = new int[6];
    static int 송신수 = 0, modtage_TÆL = 0, fejl_TÆL = 0;

    static int 설정읽기(int enhed_tal, int Placering) {
        enhed_VÆRDI.입출력정수쓰기(0xcf8, 0x80000000 | (enhed_tal << 11) | Placering);
        return enhed_VÆRDI.입출력정수읽기(0xcfc);
    }

    static boolean Tilrettelæg() {
        int enhed_tal = -1;
        for (int INDEKS = 0; INDEKS < 32; INDEKS++) {
            if (설정읽기(INDEKS, 0) == 0x813910ec) { enhed_tal = INDEKS; break; }
        }
        if (enhed_tal < 0) return false;
        int standardværdi = 설정읽기(enhed_tal, 0x10);
        if ((standardværdi & 1) == 0 || (standardværdi & 0xfffffffc) < 0x100 || (standardværdi & 0xfffffffc) > 65535) return false;
        입출력기준주소 = standardværdi & 0xfffc;
        int Kommando = 설정읽기(enhed_tal, 4);
        enhed_VÆRDI.입출력정수쓰기(0xcf8, 0x80000004 | (enhed_tal << 11));
        enhed_VÆRDI.입출력짧은수쓰기(0xcfc, Kommando | 5); // I/O 및 bus master Tillad_VÆRDI, PCI status_VÆRDI 비트는 건드리지 않음
        enhed_VÆRDI.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Nulstil_VÆRDI()) { 입출력기준주소 = 0; return false; }
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) enhed_mail[INDEKS] = enhed_VÆRDI.입출력바이트읽기(입출력기준주소 + INDEKS);
        return true;
    }

    static boolean Nulstil_VÆRDI() {
        enhed_VÆRDI.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Kør_2 = enhed_VÆRDI.밀리초();
        while ((enhed_VÆRDI.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (enhed_VÆRDI.밀리초() - Kør_2 > 100) return false;
        modtage_placere = 0; 송신칸 = 0;
        enhed_VÆRDI.입출력정수쓰기(입출력기준주소 + 0x30, enhed_VÆRDI.netværk_Hukommelse());
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) enhed_VÆRDI.입출력정수쓰기(입출력기준주소 + 0x20 + INDEKS * 4, enhed_VÆRDI.netværk_Hukommelse() + 12288);
        enhed_VÆRDI.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        enhed_VÆRDI.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        enhed_VÆRDI.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        enhed_VÆRDI.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/udsende_VÆRDI, wrap 연속 Store_VÆRDI, 8KiB
        enhed_VÆRDI.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int maile(int[] data, int varighed_VÆRDI) {
        if (입출력기준주소 == 0) return -19;
        if (varighed_VÆRDI < 14 || varighed_VÆRDI > 1514) return -90;
        int status_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Kør_2 = enhed_VÆRDI.밀리초();
        while ((enhed_VÆRDI.입출력정수읽기(status_port) & 0x2000) == 0)
            if (enhed_VÆRDI.밀리초() - Kør_2 > 100) return -110;
        int Størrelse = varighed_VÆRDI < 60 ? 60 : varighed_VÆRDI;
        for (int INDEKS = 0; INDEKS < Størrelse; INDEKS++)
            enhed_VÆRDI.skrive_Hukommelse(enhed_VÆRDI.netværk_Hukommelse() + 12288 + INDEKS, INDEKS < varighed_VÆRDI ? data[INDEKS] : 0);
        enhed_VÆRDI.입출력정수쓰기(status_port, Størrelse | 0x00080000);
        Kør_2 = enhed_VÆRDI.밀리초();
        while ((enhed_VÆRDI.입출력정수읽기(status_port) & 0xe0008000) == 0)
            if (enhed_VÆRDI.밀리초() - Kør_2 > 100) return -110;
        if ((enhed_VÆRDI.입출력정수읽기(status_port) & 0x8000) == 0) { fejl_TÆL++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return varighed_VÆRDI;
    }

    static int modtage(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((enhed_VÆRDI.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            fejl_TÆL++;
            if (!Nulstil_VÆRDI()) 입출력기준주소 = 0;
            return 0;
        }
        if ((enhed_VÆRDI.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = enhed_VÆRDI.netværk_Hukommelse() + modtage_placere;
        int status_VÆRDI = udførelse_Leder.짧은수(머리), Størrelse = udførelse_Leder.짧은수(머리 + 2);
        if (Størrelse == 0xfff0) return 0; // DMA 진행 중
        if (Størrelse < 4 || Størrelse > 1518) {
            fejl_TÆL++;
            if (!Nulstil_VÆRDI()) 입출력기준주소 = 0;
            return 0;
        }
        int varighed_VÆRDI = Størrelse - 4;
        if ((status_VÆRDI & 1) != 0) {
            for (int INDEKS = 0; INDEKS < varighed_VÆRDI; INDEKS++) data[INDEKS] = enhed_VÆRDI.기억읽기(머리 + 4 + INDEKS);
            modtage_TÆL++;
        } else { varighed_VÆRDI = 0; fejl_TÆL++; }
        modtage_placere = (modtage_placere + Størrelse + 4 + 3) & ~3;
        modtage_placere &= 8191;
        enhed_VÆRDI.입출력짧은수쓰기(입출력기준주소 + 0x38, (modtage_placere - 16) & 65535);
        enhed_VÆRDI.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return varighed_VÆRDI;
    }
}
