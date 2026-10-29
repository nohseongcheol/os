// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 skicka_värde_f993dacd 버퍼와 8KiB få_värde Loop_värde. 인터럽트 대신 폴링한다. */
public final class nätverk_drivrutin {
    static int 입출력기준주소 = 0;
    static int få_placera = 0, 송신칸 = 0;
    static int[] enhet_ADRESS = new int[6];
    static int 송신수 = 0, få_ANTAL = 0, fel_ANTAL = 0;

    static int läsa_Inställningar(int enhet_nummer, int position) {
        enhet_värde.입출력정수쓰기(0xcf8, 0x80000000 | (enhet_nummer << 11) | position);
        return enhet_värde.입출력정수읽기(0xcfc);
    }

    static boolean Förbereda() {
        int enhet_nummer = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (läsa_Inställningar(INDEX, 0) == 0x813910ec) { enhet_nummer = INDEX; break; }
        }
        if (enhet_nummer < 0) return false;
        int standardvärde = läsa_Inställningar(enhet_nummer, 0x10);
        if ((standardvärde & 1) == 0 || (standardvärde & 0xfffffffc) < 0x100 || (standardvärde & 0xfffffffc) > 65535) return false;
        입출력기준주소 = standardvärde & 0xfffc;
        int kommando = läsa_Inställningar(enhet_nummer, 4);
        enhet_värde.입출력정수쓰기(0xcf8, 0x80000004 | (enhet_nummer << 11));
        enhet_värde.입출력짧은수쓰기(0xcfc, kommando | 5); // I/O 및 bus master Tillåt_värde, PCI status_värde 비트는 건드리지 않음
        enhet_värde.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!återställ_värde()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) enhet_ADRESS[INDEX] = enhet_värde.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean återställ_värde() {
        enhet_värde.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Kör = enhet_värde.밀리초();
        while ((enhet_värde.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (enhet_värde.밀리초() - Kör > 100) return false;
        få_placera = 0; 송신칸 = 0;
        enhet_värde.입출력정수쓰기(입출력기준주소 + 0x30, enhet_värde.nätverk_Minne());
        for (int INDEX = 0; INDEX < 4; INDEX++) enhet_värde.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, enhet_värde.nätverk_Minne() + 12288);
        enhet_värde.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        enhet_värde.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        enhet_värde.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        enhet_värde.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/sänd_värde, wrap 연속 Store_värde, 8KiB
        enhet_värde.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int skicka(int[] data, int längd_värde) {
        if (입출력기준주소 == 0) return -19;
        if (längd_värde < 14 || längd_värde > 1514) return -90;
        int status_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Kör = enhet_värde.밀리초();
        while ((enhet_värde.입출력정수읽기(status_port) & 0x2000) == 0)
            if (enhet_värde.밀리초() - Kör > 100) return -110;
        int Storlek = längd_värde < 60 ? 60 : längd_värde;
        for (int INDEX = 0; INDEX < Storlek; INDEX++)
            enhet_värde.skriva_Minne(enhet_värde.nätverk_Minne() + 12288 + INDEX, INDEX < längd_värde ? data[INDEX] : 0);
        enhet_värde.입출력정수쓰기(status_port, Storlek | 0x00080000);
        Kör = enhet_värde.밀리초();
        while ((enhet_värde.입출력정수읽기(status_port) & 0xe0008000) == 0)
            if (enhet_värde.밀리초() - Kör > 100) return -110;
        if ((enhet_värde.입출력정수읽기(status_port) & 0x8000) == 0) { fel_ANTAL++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return längd_värde;
    }

    static int få(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((enhet_värde.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            fel_ANTAL++;
            if (!återställ_värde()) 입출력기준주소 = 0;
            return 0;
        }
        if ((enhet_värde.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = enhet_värde.nätverk_Minne() + få_placera;
        int status_värde = körning_Ansvarig.짧은수(머리), Storlek = körning_Ansvarig.짧은수(머리 + 2);
        if (Storlek == 0xfff0) return 0; // DMA 진행 중
        if (Storlek < 4 || Storlek > 1518) {
            fel_ANTAL++;
            if (!återställ_värde()) 입출력기준주소 = 0;
            return 0;
        }
        int längd_värde = Storlek - 4;
        if ((status_värde & 1) != 0) {
            for (int INDEX = 0; INDEX < längd_värde; INDEX++) data[INDEX] = enhet_värde.läsa_Minne(머리 + 4 + INDEX);
            få_ANTAL++;
        } else { längd_värde = 0; fel_ANTAL++; }
        få_placera = (få_placera + Storlek + 4 + 3) & ~3;
        få_placera &= 8191;
        enhet_värde.입출력짧은수쓰기(입출력기준주소 + 0x38, (få_placera - 16) & 65535);
        enhet_värde.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return längd_värde;
    }
}
