// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 sende_VERDI_f993dacd 버퍼와 8KiB motta_VERDI Loop_VERDI. 인터럽트 대신 폴링한다. */
public final class nettverk_driver {
    static int 입출력기준주소 = 0;
    static int motta_plassere = 0, 송신칸 = 0;
    static int[] enhet_e_post = new int[6];
    static int 송신수 = 0, motta_ANTALL = 0, feil_ANTALL = 0;

    static int 설정읽기(int enhet_nummer, int Posisjon) {
        enhet_VERDI.입출력정수쓰기(0xcf8, 0x80000000 | (enhet_nummer << 11) | Posisjon);
        return enhet_VERDI.입출력정수읽기(0xcfc);
    }

    static boolean Forbered() {
        int enhet_nummer = -1;
        for (int INDEKS = 0; INDEKS < 32; INDEKS++) {
            if (설정읽기(INDEKS, 0) == 0x813910ec) { enhet_nummer = INDEKS; break; }
        }
        if (enhet_nummer < 0) return false;
        int standardverdi = 설정읽기(enhet_nummer, 0x10);
        if ((standardverdi & 1) == 0 || (standardverdi & 0xfffffffc) < 0x100 || (standardverdi & 0xfffffffc) > 65535) return false;
        입출력기준주소 = standardverdi & 0xfffc;
        int Kommando = 설정읽기(enhet_nummer, 4);
        enhet_VERDI.입출력정수쓰기(0xcf8, 0x80000004 | (enhet_nummer << 11));
        enhet_VERDI.입출력짧은수쓰기(0xcfc, Kommando | 5); // I/O 및 bus master Tillat_VERDI, PCI status_VERDI 비트는 건드리지 않음
        enhet_VERDI.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!tilbakestill_VERDI()) { 입출력기준주소 = 0; return false; }
        for (int INDEKS = 0; INDEKS < 6; INDEKS++) enhet_e_post[INDEKS] = enhet_VERDI.입출력바이트읽기(입출력기준주소 + INDEKS);
        return true;
    }

    static boolean tilbakestill_VERDI() {
        enhet_VERDI.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Kjør_2 = enhet_VERDI.밀리초();
        while ((enhet_VERDI.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (enhet_VERDI.밀리초() - Kjør_2 > 100) return false;
        motta_plassere = 0; 송신칸 = 0;
        enhet_VERDI.입출력정수쓰기(입출력기준주소 + 0x30, enhet_VERDI.nettverk_Minne());
        for (int INDEKS = 0; INDEKS < 4; INDEKS++) enhet_VERDI.입출력정수쓰기(입출력기준주소 + 0x20 + INDEKS * 4, enhet_VERDI.nettverk_Minne() + 12288);
        enhet_VERDI.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        enhet_VERDI.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        enhet_VERDI.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        enhet_VERDI.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/kringkaste_VERDI, wrap 연속 Store_VERDI, 8KiB
        enhet_VERDI.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int sende(int[] data, int lengde_VERDI) {
        if (입출력기준주소 == 0) return -19;
        if (lengde_VERDI < 14 || lengde_VERDI > 1514) return -90;
        int status_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Kjør_2 = enhet_VERDI.밀리초();
        while ((enhet_VERDI.입출력정수읽기(status_port) & 0x2000) == 0)
            if (enhet_VERDI.밀리초() - Kjør_2 > 100) return -110;
        int Størrelse = lengde_VERDI < 60 ? 60 : lengde_VERDI;
        for (int INDEKS = 0; INDEKS < Størrelse; INDEKS++)
            enhet_VERDI.skrive_Minne(enhet_VERDI.nettverk_Minne() + 12288 + INDEKS, INDEKS < lengde_VERDI ? data[INDEKS] : 0);
        enhet_VERDI.입출력정수쓰기(status_port, Størrelse | 0x00080000);
        Kjør_2 = enhet_VERDI.밀리초();
        while ((enhet_VERDI.입출력정수읽기(status_port) & 0xe0008000) == 0)
            if (enhet_VERDI.밀리초() - Kjør_2 > 100) return -110;
        if ((enhet_VERDI.입출력정수읽기(status_port) & 0x8000) == 0) { feil_ANTALL++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return lengde_VERDI;
    }

    static int motta(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((enhet_VERDI.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            feil_ANTALL++;
            if (!tilbakestill_VERDI()) 입출력기준주소 = 0;
            return 0;
        }
        if ((enhet_VERDI.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = enhet_VERDI.nettverk_Minne() + motta_plassere;
        int status_VERDI = kjøring_overordnet.짧은수(머리), Størrelse = kjøring_overordnet.짧은수(머리 + 2);
        if (Størrelse == 0xfff0) return 0; // DMA 진행 중
        if (Størrelse < 4 || Størrelse > 1518) {
            feil_ANTALL++;
            if (!tilbakestill_VERDI()) 입출력기준주소 = 0;
            return 0;
        }
        int lengde_VERDI = Størrelse - 4;
        if ((status_VERDI & 1) != 0) {
            for (int INDEKS = 0; INDEKS < lengde_VERDI; INDEKS++) data[INDEKS] = enhet_VERDI.기억읽기(머리 + 4 + INDEKS);
            motta_ANTALL++;
        } else { lengde_VERDI = 0; feil_ANTALL++; }
        motta_plassere = (motta_plassere + Størrelse + 4 + 3) & ~3;
        motta_plassere &= 8191;
        enhet_VERDI.입출력짧은수쓰기(입출력기준주소 + 0x38, (motta_plassere - 16) & 65535);
        enhet_VERDI.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return lengde_VERDI;
    }
}
