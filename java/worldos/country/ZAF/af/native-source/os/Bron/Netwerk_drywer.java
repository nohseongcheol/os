// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 e_pos_VALUE 버퍼와 8KiB 수신 lus_VALUE. 인터럽트 대신 폴링한다. */
public final class Netwerk_drywer {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] mobiel_adres = new int[6];
    static int 송신수 = 0, 수신수 = 0, fout_COUNT = 0;

    static int 설정읽기(int 장치번호, int Posisie) {
        mobiel_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Posisie);
        return mobiel_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Maak_gereed() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int verstekwaarde = 설정읽기(장치번호, 0x10);
        if ((verstekwaarde & 1) == 0 || (verstekwaarde & 0xfffffffc) < 0x100 || (verstekwaarde & 0xfffffffc) > 65535) return false;
        입출력기준주소 = verstekwaarde & 0xfffc;
        int Opdrag = 설정읽기(장치번호, 4);
        mobiel_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        mobiel_VALUE.입출력짧은수쓰기(0xcfc, Opdrag | 5); // I/O 및 bus master toelaat_VALUE, PCI stand_VALUE 비트는 건드리지 않음
        mobiel_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!stel_weer_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) mobiel_adres[INDEX] = mobiel_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean stel_weer_VALUE() {
        mobiel_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Loop = mobiel_VALUE.밀리초();
        while ((mobiel_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (mobiel_VALUE.밀리초() - Loop > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        mobiel_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, mobiel_VALUE.Netwerk_Geheue());
        for (int INDEX = 0; INDEX < 4; INDEX++) mobiel_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, mobiel_VALUE.Netwerk_Geheue() + 12288);
        mobiel_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        mobiel_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        mobiel_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        mobiel_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/uitsaai_VALUE, wrap 연속 bêre_VALUE, 8KiB
        mobiel_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int e_pos(int[] data, int lengte_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (lengte_VALUE < 14 || lengte_VALUE > 1514) return -90;
        int stand_ombou = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Loop = mobiel_VALUE.밀리초();
        while ((mobiel_VALUE.입출력정수읽기(stand_ombou) & 0x2000) == 0)
            if (mobiel_VALUE.밀리초() - Loop > 100) return -110;
        int Grootte = lengte_VALUE < 60 ? 60 : lengte_VALUE;
        for (int INDEX = 0; INDEX < Grootte; INDEX++)
            mobiel_VALUE.skryf_Geheue(mobiel_VALUE.Netwerk_Geheue() + 12288 + INDEX, INDEX < lengte_VALUE ? data[INDEX] : 0);
        mobiel_VALUE.입출력정수쓰기(stand_ombou, Grootte | 0x00080000);
        Loop = mobiel_VALUE.밀리초();
        while ((mobiel_VALUE.입출력정수읽기(stand_ombou) & 0xe0008000) == 0)
            if (mobiel_VALUE.밀리초() - Loop > 100) return -110;
        if ((mobiel_VALUE.입출력정수읽기(stand_ombou) & 0x8000) == 0) { fout_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return lengte_VALUE;
    }

    static int 받기(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((mobiel_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            fout_COUNT++;
            if (!stel_weer_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((mobiel_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = mobiel_VALUE.Netwerk_Geheue() + 수신위치;
        int stand_VALUE = 실행관리.짧은수(머리), Grootte = 실행관리.짧은수(머리 + 2);
        if (Grootte == 0xfff0) return 0; // DMA 진행 중
        if (Grootte < 4 || Grootte > 1518) {
            fout_COUNT++;
            if (!stel_weer_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int lengte_VALUE = Grootte - 4;
        if ((stand_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < lengte_VALUE; INDEX++) data[INDEX] = mobiel_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { lengte_VALUE = 0; fout_COUNT++; }
        수신위치 = (수신위치 + Grootte + 4 + 3) & ~3;
        수신위치 &= 8191;
        mobiel_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        mobiel_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return lengte_VALUE;
    }
}
