// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 neldude_njaru 버퍼와 8KiB 수신 kowal_njaru. 인터럽트 대신 폴링한다. */
public final class laylaytol_pilot {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] kaɓirgal_ñiiɓirde = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        kaɓirgal_njaru.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return kaɓirgal_njaru.입출력정수읽기(0xcfc);
    }

    static boolean Heblu() {
        int 장치번호 = -1;
        for (int joopirdu = 0; joopirdu < 32; joopirdu++) {
            if (설정읽기(joopirdu, 0) == 0x813910ec) { 장치번호 = joopirdu; break; }
        }
        if (장치번호 < 0) return false;
        int lasli_njaru = 설정읽기(장치번호, 0x10);
        if ((lasli_njaru & 1) == 0 || (lasli_njaru & 0xfffffffc) < 0x100 || (lasli_njaru & 0xfffffffc) > 65535) return false;
        입출력기준주소 = lasli_njaru & 0xfffc;
        int ginol = 설정읽기(장치번호, 4);
        kaɓirgal_njaru.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        kaɓirgal_njaru.입출력짧은수쓰기(0xcfc, ginol | 5); // I/O 및 bus master Wellit_njaru, PCI ngonka_njaru 비트는 건드리지 않음
        kaɓirgal_njaru.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!waɗtude_no_waano_njaru()) { 입출력기준주소 = 0; return false; }
        for (int joopirdu = 0; joopirdu < 6; joopirdu++) kaɓirgal_ñiiɓirde[joopirdu] = kaɓirgal_njaru.입출력바이트읽기(입출력기준주소 + joopirdu);
        return true;
    }

    static boolean waɗtude_no_waano_njaru() {
        kaɓirgal_njaru.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int huutoraade = kaɓirgal_njaru.밀리초();
        while ((kaɓirgal_njaru.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (kaɓirgal_njaru.밀리초() - huutoraade > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        kaɓirgal_njaru.입출력정수쓰기(입출력기준주소 + 0x30, kaɓirgal_njaru.laylaytol_teskordu());
        for (int joopirdu = 0; joopirdu < 4; joopirdu++) kaɓirgal_njaru.입출력정수쓰기(입출력기준주소 + 0x20 + joopirdu * 4, kaɓirgal_njaru.laylaytol_teskordu() + 12288);
        kaɓirgal_njaru.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        kaɓirgal_njaru.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        kaɓirgal_njaru.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        kaɓirgal_njaru.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/방송, wrap 연속 resde_njaru, 8KiB
        kaɓirgal_njaru.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int neldude(int[] keɓe, int njuuteendi_njaru) {
        if (입출력기준주소 == 0) return -19;
        if (njuuteendi_njaru < 14 || njuuteendi_njaru > 1514) return -90;
        int ngonka_poor = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int huutoraade = kaɓirgal_njaru.밀리초();
        while ((kaɓirgal_njaru.입출력정수읽기(ngonka_poor) & 0x2000) == 0)
            if (kaɓirgal_njaru.밀리초() - huutoraade > 100) return -110;
        int waylude_etannde = njuuteendi_njaru < 60 ? 60 : njuuteendi_njaru;
        for (int joopirdu = 0; joopirdu < waylude_etannde; joopirdu++)
            kaɓirgal_njaru.winndude_teskordu(kaɓirgal_njaru.laylaytol_teskordu() + 12288 + joopirdu, joopirdu < njuuteendi_njaru ? keɓe[joopirdu] : 0);
        kaɓirgal_njaru.입출력정수쓰기(ngonka_poor, waylude_etannde | 0x00080000);
        huutoraade = kaɓirgal_njaru.밀리초();
        while ((kaɓirgal_njaru.입출력정수읽기(ngonka_poor) & 0xe0008000) == 0)
            if (kaɓirgal_njaru.밀리초() - huutoraade > 100) return -110;
        if ((kaɓirgal_njaru.입출력정수읽기(ngonka_poor) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return njuuteendi_njaru;
    }

    static int 받기(int[] keɓe) {
        if (입출력기준주소 == 0) return 0;
        if ((kaɓirgal_njaru.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!waɗtude_no_waano_njaru()) 입출력기준주소 = 0;
            return 0;
        }
        if ((kaɓirgal_njaru.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = kaɓirgal_njaru.laylaytol_teskordu() + 수신위치;
        int ngonka_njaru = 실행관리.짧은수(머리), waylude_etannde = 실행관리.짧은수(머리 + 2);
        if (waylude_etannde == 0xfff0) return 0; // DMA 진행 중
        if (waylude_etannde < 4 || waylude_etannde > 1518) {
            오류수++;
            if (!waɗtude_no_waano_njaru()) 입출력기준주소 = 0;
            return 0;
        }
        int njuuteendi_njaru = waylude_etannde - 4;
        if ((ngonka_njaru & 1) != 0) {
            for (int joopirdu = 0; joopirdu < njuuteendi_njaru; joopirdu++) keɓe[joopirdu] = kaɓirgal_njaru.기억읽기(머리 + 4 + joopirdu);
            수신수++;
        } else { njuuteendi_njaru = 0; 오류수++; }
        수신위치 = (수신위치 + waylude_etannde + 4 + 3) & ~3;
        수신위치 &= 8191;
        kaɓirgal_njaru.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        kaɓirgal_njaru.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return njuuteendi_njaru;
    }
}
