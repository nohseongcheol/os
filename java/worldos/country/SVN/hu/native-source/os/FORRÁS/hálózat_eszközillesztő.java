// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 küld_ÉRTÉK 버퍼와 8KiB fogad_ÉRTÉK Loop_ÉRTÉK. 인터럽트 대신 폴링한다. */
public final class hálózat_eszközillesztő {
    static int 입출력기준주소 = 0;
    static int fogad_pozíció = 0, 송신칸 = 0;
    static int[] mobil_CÍM = new int[6];
    static int 송신수 = 0, fogad_DARAB = 0, hiba_DARAB = 0;

    static int 설정읽기(int mobil_szám, int Pozíció) {
        mobil_ÉRTÉK.입출력정수쓰기(0xcf8, 0x80000000 | (mobil_szám << 11) | Pozíció);
        return mobil_ÉRTÉK.입출력정수읽기(0xcfc);
    }

    static boolean Előkészítés() {
        int mobil_szám = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { mobil_szám = INDEX; break; }
        }
        if (mobil_szám < 0) return false;
        int alapértelmezett_érték = 설정읽기(mobil_szám, 0x10);
        if ((alapértelmezett_érték & 1) == 0 || (alapértelmezett_érték & 0xfffffffc) < 0x100 || (alapértelmezett_érték & 0xfffffffc) > 65535) return false;
        입출력기준주소 = alapértelmezett_érték & 0xfffc;
        int Parancs = 설정읽기(mobil_szám, 4);
        mobil_ÉRTÉK.입출력정수쓰기(0xcf8, 0x80000004 | (mobil_szám << 11));
        mobil_ÉRTÉK.입출력짧은수쓰기(0xcfc, Parancs | 5); // I/O 및 bus master engedélyez_ÉRTÉK, PCI Állapot_ÉRTÉK 비트는 건드리지 않음
        mobil_ÉRTÉK.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!átállít_ÉRTÉK()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) mobil_CÍM[INDEX] = mobil_ÉRTÉK.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean átállít_ÉRTÉK() {
        mobil_ÉRTÉK.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Futtatás = mobil_ÉRTÉK.밀리초();
        while ((mobil_ÉRTÉK.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (mobil_ÉRTÉK.밀리초() - Futtatás > 100) return false;
        fogad_pozíció = 0; 송신칸 = 0;
        mobil_ÉRTÉK.입출력정수쓰기(입출력기준주소 + 0x30, mobil_ÉRTÉK.hálózat_Memória());
        for (int INDEX = 0; INDEX < 4; INDEX++) mobil_ÉRTÉK.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, mobil_ÉRTÉK.hálózat_Memória() + 12288);
        mobil_ÉRTÉK.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        mobil_ÉRTÉK.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        mobil_ÉRTÉK.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        mobil_ÉRTÉK.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/adás_ÉRTÉK, wrap 연속 tár_ÉRTÉK, 8KiB
        mobil_ÉRTÉK.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int küld(int[] adat, int hossz_ÉRTÉK) {
        if (입출력기준주소 == 0) return -19;
        if (hossz_ÉRTÉK < 14 || hossz_ÉRTÉK > 1514) return -90;
        int állapot_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Futtatás = mobil_ÉRTÉK.밀리초();
        while ((mobil_ÉRTÉK.입출력정수읽기(állapot_port) & 0x2000) == 0)
            if (mobil_ÉRTÉK.밀리초() - Futtatás > 100) return -110;
        int Méret = hossz_ÉRTÉK < 60 ? 60 : hossz_ÉRTÉK;
        for (int INDEX = 0; INDEX < Méret; INDEX++)
            mobil_ÉRTÉK.ír_Memória(mobil_ÉRTÉK.hálózat_Memória() + 12288 + INDEX, INDEX < hossz_ÉRTÉK ? adat[INDEX] : 0);
        mobil_ÉRTÉK.입출력정수쓰기(állapot_port, Méret | 0x00080000);
        Futtatás = mobil_ÉRTÉK.밀리초();
        while ((mobil_ÉRTÉK.입출력정수읽기(állapot_port) & 0xe0008000) == 0)
            if (mobil_ÉRTÉK.밀리초() - Futtatás > 100) return -110;
        if ((mobil_ÉRTÉK.입출력정수읽기(állapot_port) & 0x8000) == 0) { hiba_DARAB++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return hossz_ÉRTÉK;
    }

    static int fogad(int[] adat) {
        if (입출력기준주소 == 0) return 0;
        if ((mobil_ÉRTÉK.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            hiba_DARAB++;
            if (!átállít_ÉRTÉK()) 입출력기준주소 = 0;
            return 0;
        }
        if ((mobil_ÉRTÉK.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = mobil_ÉRTÉK.hálózat_Memória() + fogad_pozíció;
        int Állapot_ÉRTÉK = végrehajtás_kezelő.짧은수(머리), Méret = végrehajtás_kezelő.짧은수(머리 + 2);
        if (Méret == 0xfff0) return 0; // DMA 진행 중
        if (Méret < 4 || Méret > 1518) {
            hiba_DARAB++;
            if (!átállít_ÉRTÉK()) 입출력기준주소 = 0;
            return 0;
        }
        int hossz_ÉRTÉK = Méret - 4;
        if ((Állapot_ÉRTÉK & 1) != 0) {
            for (int INDEX = 0; INDEX < hossz_ÉRTÉK; INDEX++) adat[INDEX] = mobil_ÉRTÉK.기억읽기(머리 + 4 + INDEX);
            fogad_DARAB++;
        } else { hossz_ÉRTÉK = 0; hiba_DARAB++; }
        fogad_pozíció = (fogad_pozíció + Méret + 4 + 3) & ~3;
        fogad_pozíció &= 8191;
        mobil_ÉRTÉK.입출력짧은수쓰기(입출력기준주소 + 0x38, (fogad_pozíció - 16) & 65535);
        mobil_ÉRTÉK.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return hossz_ÉRTÉK;
    }
}
