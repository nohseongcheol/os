// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 sūtīt_VALUE 버퍼와 8KiB saņemt_VALUE Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class tīkls_draiveris {
    static int 입출력기준주소 = 0;
    static int saņemt_amats = 0, 송신칸 = 0;
    static int[] ierīce_adrese = new int[6];
    static int 송신수 = 0, saņemt_COUNT = 0, kļūda_COUNT = 0;

    static int 설정읽기(int ierīce_numurs, int Novietojums) {
        ierīce_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (ierīce_numurs << 11) | Novietojums);
        return ierīce_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Sagatavot() {
        int ierīce_numurs = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { ierīce_numurs = INDEX; break; }
        }
        if (ierīce_numurs < 0) return false;
        int noklusējuma_vērtība = 설정읽기(ierīce_numurs, 0x10);
        if ((noklusējuma_vērtība & 1) == 0 || (noklusējuma_vērtība & 0xfffffffc) < 0x100 || (noklusējuma_vērtība & 0xfffffffc) > 65535) return false;
        입출력기준주소 = noklusējuma_vērtība & 0xfffc;
        int Komanda = 설정읽기(ierīce_numurs, 4);
        ierīce_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (ierīce_numurs << 11));
        ierīce_VALUE.입출력짧은수쓰기(0xcfc, Komanda | 5); // I/O 및 bus master Atļaut_VALUE, PCI Statuss_VALUE 비트는 건드리지 않음
        ierīce_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!atiestatīt_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) ierīce_adrese[INDEX] = ierīce_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean atiestatīt_VALUE() {
        ierīce_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Palaist = ierīce_VALUE.밀리초();
        while ((ierīce_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (ierīce_VALUE.밀리초() - Palaist > 100) return false;
        saņemt_amats = 0; 송신칸 = 0;
        ierīce_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, ierīce_VALUE.tīkls_atmiņa());
        for (int INDEX = 0; INDEX < 4; INDEX++) ierīce_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, ierīce_VALUE.tīkls_atmiņa() + 12288);
        ierīce_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        ierīce_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        ierīce_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        ierīce_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/apraide_VALUE, wrap 연속 Store_VALUE, 8KiB
        ierīce_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int sūtīt(int[] dati, int 길이) {
        if (입출력기준주소 == 0) return -19;
        if (길이 < 14 || 길이 > 1514) return -90;
        int statuss_ports = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Palaist = ierīce_VALUE.밀리초();
        while ((ierīce_VALUE.입출력정수읽기(statuss_ports) & 0x2000) == 0)
            if (ierīce_VALUE.밀리초() - Palaist > 100) return -110;
        int Izmērs = 길이 < 60 ? 60 : 길이;
        for (int INDEX = 0; INDEX < Izmērs; INDEX++)
            ierīce_VALUE.rakstīšana_atmiņa(ierīce_VALUE.tīkls_atmiņa() + 12288 + INDEX, INDEX < 길이 ? dati[INDEX] : 0);
        ierīce_VALUE.입출력정수쓰기(statuss_ports, Izmērs | 0x00080000);
        Palaist = ierīce_VALUE.밀리초();
        while ((ierīce_VALUE.입출력정수읽기(statuss_ports) & 0xe0008000) == 0)
            if (ierīce_VALUE.밀리초() - Palaist > 100) return -110;
        if ((ierīce_VALUE.입출력정수읽기(statuss_ports) & 0x8000) == 0) { kļūda_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return 길이;
    }

    static int saņemt(int[] dati) {
        if (입출력기준주소 == 0) return 0;
        if ((ierīce_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            kļūda_COUNT++;
            if (!atiestatīt_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((ierīce_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = ierīce_VALUE.tīkls_atmiņa() + saņemt_amats;
        int Statuss_VALUE = 실행관리.짧은수(머리), Izmērs = 실행관리.짧은수(머리 + 2);
        if (Izmērs == 0xfff0) return 0; // DMA 진행 중
        if (Izmērs < 4 || Izmērs > 1518) {
            kļūda_COUNT++;
            if (!atiestatīt_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int 길이 = Izmērs - 4;
        if ((Statuss_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < 길이; INDEX++) dati[INDEX] = ierīce_VALUE.기억읽기(머리 + 4 + INDEX);
            saņemt_COUNT++;
        } else { 길이 = 0; kļūda_COUNT++; }
        saņemt_amats = (saņemt_amats + Izmērs + 4 + 3) & ~3;
        saņemt_amats &= 8191;
        ierīce_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (saņemt_amats - 16) & 65535);
        ierīce_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return 길이;
    }
}
