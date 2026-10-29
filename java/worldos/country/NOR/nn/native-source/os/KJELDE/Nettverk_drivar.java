// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 sende_VALUE_f993dacd 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class Nettverk_drivar {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] mobil_ADDRESS = new int[6];
    static int 송신수 = 0, 수신수 = 0, feil_COUNT = 0;

    static int 설정읽기(int 장치번호, int Posisjon) {
        mobil_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Posisjon);
        return mobil_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Klargjer() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int standardverdi = 설정읽기(장치번호, 0x10);
        if ((standardverdi & 1) == 0 || (standardverdi & 0xfffffffc) < 0x100 || (standardverdi & 0xfffffffc) > 65535) return false;
        입출력기준주소 = standardverdi & 0xfffc;
        int Kommando = 설정읽기(장치번호, 4);
        mobil_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        mobil_VALUE.입출력짧은수쓰기(0xcfc, Kommando | 5); // I/O 및 bus master Tillat_VALUE, PCI status_VALUE 비트는 건드리지 않음
        mobil_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!tilbakestill_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) mobil_ADDRESS[INDEX] = mobil_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean tilbakestill_VALUE() {
        mobil_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Køyr_2 = mobil_VALUE.밀리초();
        while ((mobil_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (mobil_VALUE.밀리초() - Køyr_2 > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, mobil_VALUE.Nettverk_Minne());
        for (int INDEX = 0; INDEX < 4; INDEX++) mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, mobil_VALUE.Nettverk_Minne() + 12288);
        mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        mobil_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/kringkasting_VALUE, wrap 연속 Store_VALUE, 8KiB
        mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int sende(int[] data, int lengd_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (lengd_VALUE < 14 || lengd_VALUE > 1514) return -90;
        int merkje_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Køyr_2 = mobil_VALUE.밀리초();
        while ((mobil_VALUE.입출력정수읽기(merkje_port) & 0x2000) == 0)
            if (mobil_VALUE.밀리초() - Køyr_2 > 100) return -110;
        int Storleik = lengd_VALUE < 60 ? 60 : lengd_VALUE;
        for (int INDEX = 0; INDEX < Storleik; INDEX++)
            mobil_VALUE.skrive_Minne(mobil_VALUE.Nettverk_Minne() + 12288 + INDEX, INDEX < lengd_VALUE ? data[INDEX] : 0);
        mobil_VALUE.입출력정수쓰기(merkje_port, Storleik | 0x00080000);
        Køyr_2 = mobil_VALUE.밀리초();
        while ((mobil_VALUE.입출력정수읽기(merkje_port) & 0xe0008000) == 0)
            if (mobil_VALUE.밀리초() - Køyr_2 > 100) return -110;
        if ((mobil_VALUE.입출력정수읽기(merkje_port) & 0x8000) == 0) { feil_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return lengd_VALUE;
    }

    static int 받기(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((mobil_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            feil_COUNT++;
            if (!tilbakestill_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((mobil_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = mobil_VALUE.Nettverk_Minne() + 수신위치;
        int status_VALUE = 실행관리.짧은수(머리), Storleik = 실행관리.짧은수(머리 + 2);
        if (Storleik == 0xfff0) return 0; // DMA 진행 중
        if (Storleik < 4 || Storleik > 1518) {
            feil_COUNT++;
            if (!tilbakestill_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int lengd_VALUE = Storleik - 4;
        if ((status_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < lengd_VALUE; INDEX++) data[INDEX] = mobil_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { lengd_VALUE = 0; feil_COUNT++; }
        수신위치 = (수신위치 + Storleik + 4 + 3) & ~3;
        수신위치 &= 8191;
        mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return lengd_VALUE;
    }
}
