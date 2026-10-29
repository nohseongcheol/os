// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 dërgoj_VALUE 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class rrjet_drejtues {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] pajisje_email = new int[6];
    static int 송신수 = 0, 수신수 = 0, gabim_COUNT = 0;

    static int 설정읽기(int 장치번호, int Pozicioni) {
        pajisje_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Pozicioni);
        return pajisje_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Përgatit() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int vlerë_e_parazgjedhur = 설정읽기(장치번호, 0x10);
        if ((vlerë_e_parazgjedhur & 1) == 0 || (vlerë_e_parazgjedhur & 0xfffffffc) < 0x100 || (vlerë_e_parazgjedhur & 0xfffffffc) > 65535) return false;
        입출력기준주소 = vlerë_e_parazgjedhur & 0xfffc;
        int Komanda = 설정읽기(장치번호, 4);
        pajisje_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        pajisje_VALUE.입출력짧은수쓰기(0xcfc, Komanda | 5); // I/O 및 bus master Lejoj_VALUE, PCI status_VALUE 비트는 건드리지 않음
        pajisje_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Rivendos_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) pajisje_email[INDEX] = pajisje_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean Rivendos_VALUE() {
        pajisje_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Ekzekuto = pajisje_VALUE.밀리초();
        while ((pajisje_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (pajisje_VALUE.밀리초() - Ekzekuto > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        pajisje_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, pajisje_VALUE.rrjet_Memorie());
        for (int INDEX = 0; INDEX < 4; INDEX++) pajisje_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, pajisje_VALUE.rrjet_Memorie() + 12288);
        pajisje_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        pajisje_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        pajisje_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        pajisje_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/transmetoj_VALUE, wrap 연속 Store_VALUE, 8KiB
        pajisje_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int dërgoj(int[] të_dhëna, int gjatësi_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (gjatësi_VALUE < 14 || gjatësi_VALUE > 1514) return -90;
        int status_portë = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Ekzekuto = pajisje_VALUE.밀리초();
        while ((pajisje_VALUE.입출력정수읽기(status_portë) & 0x2000) == 0)
            if (pajisje_VALUE.밀리초() - Ekzekuto > 100) return -110;
        int Madhësi = gjatësi_VALUE < 60 ? 60 : gjatësi_VALUE;
        for (int INDEX = 0; INDEX < Madhësi; INDEX++)
            pajisje_VALUE.shkruaj_Memorie(pajisje_VALUE.rrjet_Memorie() + 12288 + INDEX, INDEX < gjatësi_VALUE ? të_dhëna[INDEX] : 0);
        pajisje_VALUE.입출력정수쓰기(status_portë, Madhësi | 0x00080000);
        Ekzekuto = pajisje_VALUE.밀리초();
        while ((pajisje_VALUE.입출력정수읽기(status_portë) & 0xe0008000) == 0)
            if (pajisje_VALUE.밀리초() - Ekzekuto > 100) return -110;
        if ((pajisje_VALUE.입출력정수읽기(status_portë) & 0x8000) == 0) { gabim_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return gjatësi_VALUE;
    }

    static int 받기(int[] të_dhëna) {
        if (입출력기준주소 == 0) return 0;
        if ((pajisje_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            gabim_COUNT++;
            if (!Rivendos_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((pajisje_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = pajisje_VALUE.rrjet_Memorie() + 수신위치;
        int status_VALUE = 실행관리.짧은수(머리), Madhësi = 실행관리.짧은수(머리 + 2);
        if (Madhësi == 0xfff0) return 0; // DMA 진행 중
        if (Madhësi < 4 || Madhësi > 1518) {
            gabim_COUNT++;
            if (!Rivendos_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int gjatësi_VALUE = Madhësi - 4;
        if ((status_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < gjatësi_VALUE; INDEX++) të_dhëna[INDEX] = pajisje_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { gjatësi_VALUE = 0; gabim_COUNT++; }
        수신위치 = (수신위치 + Madhësi + 4 + 3) & ~3;
        수신위치 &= 8191;
        pajisje_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        pajisje_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return gjatësi_VALUE;
    }
}
