// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 göndermek_değer 버퍼와 8KiB almak_değer Loop_değer. 인터럽트 대신 폴링한다. */
public final class ağ_sürücü {
    static int 입출력기준주소 = 0;
    static int almak_konum = 0, 송신칸 = 0;
    static int[] cihaz_ADRES = new int[6];
    static int 송신수 = 0, almak_BAĞ_DEĞ_SAY = 0, hata_BAĞ_DEĞ_SAY = 0;

    static int 설정읽기(int 장치번호, int konum) {
        cihaz_değer.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | konum);
        return cihaz_değer.입출력정수읽기(0xcfc);
    }

    static boolean Hazırlan() {
        int 장치번호 = -1;
        for (int Dizin = 0; Dizin < 32; Dizin++) {
            if (설정읽기(Dizin, 0) == 0x813910ec) { 장치번호 = Dizin; break; }
        }
        if (장치번호 < 0) return false;
        int varsayılan_değer = 설정읽기(장치번호, 0x10);
        if ((varsayılan_değer & 1) == 0 || (varsayılan_değer & 0xfffffffc) < 0x100 || (varsayılan_değer & 0xfffffffc) > 65535) return false;
        입출력기준주소 = varsayılan_değer & 0xfffc;
        int komut = 설정읽기(장치번호, 4);
        cihaz_değer.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        cihaz_değer.입출력짧은수쓰기(0xcfc, komut | 5); // I/O 및 bus master İzin_Ver_değer, PCI Durum_değer 비트는 건드리지 않음
        cihaz_değer.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!sıfırlamak_değer()) { 입출력기준주소 = 0; return false; }
        for (int Dizin = 0; Dizin < 6; Dizin++) cihaz_ADRES[Dizin] = cihaz_değer.입출력바이트읽기(입출력기준주소 + Dizin);
        return true;
    }

    static boolean sıfırlamak_değer() {
        cihaz_değer.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int çalıştır = cihaz_değer.밀리초();
        while ((cihaz_değer.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (cihaz_değer.밀리초() - çalıştır > 100) return false;
        almak_konum = 0; 송신칸 = 0;
        cihaz_değer.입출력정수쓰기(입출력기준주소 + 0x30, cihaz_değer.ağ_Bellek());
        for (int Dizin = 0; Dizin < 4; Dizin++) cihaz_değer.입출력정수쓰기(입출력기준주소 + 0x20 + Dizin * 4, cihaz_değer.ağ_Bellek() + 12288);
        cihaz_değer.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        cihaz_değer.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        cihaz_değer.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        cihaz_değer.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/yayın_değer, wrap 연속 depo_değer, 8KiB
        cihaz_değer.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int göndermek(int[] veri, int süre_değer) {
        if (입출력기준주소 == 0) return -19;
        if (süre_değer < 14 || süre_değer > 1514) return -90;
        int Durum_taşımak = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int çalıştır = cihaz_değer.밀리초();
        while ((cihaz_değer.입출력정수읽기(Durum_taşımak) & 0x2000) == 0)
            if (cihaz_değer.밀리초() - çalıştır > 100) return -110;
        int Boyut = süre_değer < 60 ? 60 : süre_değer;
        for (int Dizin = 0; Dizin < Boyut; Dizin++)
            cihaz_değer.yazma_Bellek(cihaz_değer.ağ_Bellek() + 12288 + Dizin, Dizin < süre_değer ? veri[Dizin] : 0);
        cihaz_değer.입출력정수쓰기(Durum_taşımak, Boyut | 0x00080000);
        çalıştır = cihaz_değer.밀리초();
        while ((cihaz_değer.입출력정수읽기(Durum_taşımak) & 0xe0008000) == 0)
            if (cihaz_değer.밀리초() - çalıştır > 100) return -110;
        if ((cihaz_değer.입출력정수읽기(Durum_taşımak) & 0x8000) == 0) { hata_BAĞ_DEĞ_SAY++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return süre_değer;
    }

    static int almak(int[] veri) {
        if (입출력기준주소 == 0) return 0;
        if ((cihaz_değer.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            hata_BAĞ_DEĞ_SAY++;
            if (!sıfırlamak_değer()) 입출력기준주소 = 0;
            return 0;
        }
        if ((cihaz_değer.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = cihaz_değer.ağ_Bellek() + almak_konum;
        int Durum_değer = yürütme_yönetici.짧은수(머리), Boyut = yürütme_yönetici.짧은수(머리 + 2);
        if (Boyut == 0xfff0) return 0; // DMA 진행 중
        if (Boyut < 4 || Boyut > 1518) {
            hata_BAĞ_DEĞ_SAY++;
            if (!sıfırlamak_değer()) 입출력기준주소 = 0;
            return 0;
        }
        int süre_değer = Boyut - 4;
        if ((Durum_değer & 1) != 0) {
            for (int Dizin = 0; Dizin < süre_değer; Dizin++) veri[Dizin] = cihaz_değer.기억읽기(머리 + 4 + Dizin);
            almak_BAĞ_DEĞ_SAY++;
        } else { süre_değer = 0; hata_BAĞ_DEĞ_SAY++; }
        almak_konum = (almak_konum + Boyut + 4 + 3) & ~3;
        almak_konum &= 8191;
        cihaz_değer.입출력짧은수쓰기(입출력기준주소 + 0x38, (almak_konum - 16) & 65535);
        cihaz_değer.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return süre_değer;
    }
}
