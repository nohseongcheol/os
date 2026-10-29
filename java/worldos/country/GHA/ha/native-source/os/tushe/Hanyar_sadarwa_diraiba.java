// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 Aika_Daraja 버퍼와 8KiB 수신 Warware_Daraja. 인터럽트 대신 폴링한다. */
public final class Hanyar_sadarwa_diraiba {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] na_ura_imel = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        na_ura_Daraja.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return na_ura_Daraja.입출력정수읽기(0xcfc);
    }

    static boolean Shirya() {
        int 장치번호 = -1;
        for (int Indes = 0; Indes < 32; Indes++) {
            if (설정읽기(Indes, 0) == 0x813910ec) { 장치번호 = Indes; break; }
        }
        if (장치번호 < 0) return false;
        int Tanadaddiyar_daraja = 설정읽기(장치번호, 0x10);
        if ((Tanadaddiyar_daraja & 1) == 0 || (Tanadaddiyar_daraja & 0xfffffffc) < 0x100 || (Tanadaddiyar_daraja & 0xfffffffc) > 65535) return false;
        입출력기준주소 = Tanadaddiyar_daraja & 0xfffc;
        int Umarni = 설정읽기(장치번호, 4);
        na_ura_Daraja.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        na_ura_Daraja.입출력짧은수쓰기(0xcfc, Umarni | 5); // I/O 및 bus master Bada_izini_Daraja, PCI Matsayi_Daraja 비트는 건드리지 않음
        na_ura_Daraja.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Sake_saiti_Daraja()) { 입출력기준주소 = 0; return false; }
        for (int Indes = 0; Indes < 6; Indes++) na_ura_imel[Indes] = na_ura_Daraja.입출력바이트읽기(입출력기준주소 + Indes);
        return true;
    }

    static boolean Sake_saiti_Daraja() {
        na_ura_Daraja.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Tafiyar_da = na_ura_Daraja.밀리초();
        while ((na_ura_Daraja.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (na_ura_Daraja.밀리초() - Tafiyar_da > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        na_ura_Daraja.입출력정수쓰기(입출력기준주소 + 0x30, na_ura_Daraja.Hanyar_sadarwa_Mahardatar_kwamfuta());
        for (int Indes = 0; Indes < 4; Indes++) na_ura_Daraja.입출력정수쓰기(입출력기준주소 + 0x20 + Indes * 4, na_ura_Daraja.Hanyar_sadarwa_Mahardatar_kwamfuta() + 12288);
        na_ura_Daraja.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        na_ura_Daraja.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        na_ura_Daraja.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        na_ura_Daraja.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/watsar_da_Daraja, wrap 연속 Ajiye_Daraja, 8KiB
        na_ura_Daraja.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int Aika(int[] Tarin_bayani, int Tsawo_Daraja) {
        if (입출력기준주소 == 0) return -19;
        if (Tsawo_Daraja < 14 || Tsawo_Daraja > 1514) return -90;
        int samuwa_fot = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Tafiyar_da = na_ura_Daraja.밀리초();
        while ((na_ura_Daraja.입출력정수읽기(samuwa_fot) & 0x2000) == 0)
            if (na_ura_Daraja.밀리초() - Tafiyar_da > 100) return -110;
        int Girma = Tsawo_Daraja < 60 ? 60 : Tsawo_Daraja;
        for (int Indes = 0; Indes < Girma; Indes++)
            na_ura_Daraja.Rubuta_Mahardatar_kwamfuta(na_ura_Daraja.Hanyar_sadarwa_Mahardatar_kwamfuta() + 12288 + Indes, Indes < Tsawo_Daraja ? Tarin_bayani[Indes] : 0);
        na_ura_Daraja.입출력정수쓰기(samuwa_fot, Girma | 0x00080000);
        Tafiyar_da = na_ura_Daraja.밀리초();
        while ((na_ura_Daraja.입출력정수읽기(samuwa_fot) & 0xe0008000) == 0)
            if (na_ura_Daraja.밀리초() - Tafiyar_da > 100) return -110;
        if ((na_ura_Daraja.입출력정수읽기(samuwa_fot) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return Tsawo_Daraja;
    }

    static int 받기(int[] Tarin_bayani) {
        if (입출력기준주소 == 0) return 0;
        if ((na_ura_Daraja.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!Sake_saiti_Daraja()) 입출력기준주소 = 0;
            return 0;
        }
        if ((na_ura_Daraja.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = na_ura_Daraja.Hanyar_sadarwa_Mahardatar_kwamfuta() + 수신위치;
        int Matsayi_Daraja = 실행관리.짧은수(머리), Girma = 실행관리.짧은수(머리 + 2);
        if (Girma == 0xfff0) return 0; // DMA 진행 중
        if (Girma < 4 || Girma > 1518) {
            오류수++;
            if (!Sake_saiti_Daraja()) 입출력기준주소 = 0;
            return 0;
        }
        int Tsawo_Daraja = Girma - 4;
        if ((Matsayi_Daraja & 1) != 0) {
            for (int Indes = 0; Indes < Tsawo_Daraja; Indes++) Tarin_bayani[Indes] = na_ura_Daraja.기억읽기(머리 + 4 + Indes);
            수신수++;
        } else { Tsawo_Daraja = 0; 오류수++; }
        수신위치 = (수신위치 + Girma + 4 + 3) & ~3;
        수신위치 &= 8191;
        na_ura_Daraja.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        na_ura_Daraja.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return Tsawo_Daraja;
    }
}
