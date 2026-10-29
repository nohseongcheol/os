// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 saatma_VALUE 버퍼와 8KiB saama_VALUE Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class võrk_draiver {
    static int 입출력기준주소 = 0;
    static int saama_ametikoht = 0, 송신칸 = 0;
    static int[] seade_ADDRESS = new int[6];
    static int 송신수 = 0, saama_COUNT = 0, tõrge_COUNT = 0;

    static int 설정읽기(int seade_number, int Asukoht) {
        seade_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (seade_number << 11) | Asukoht);
        return seade_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Ettevalmistamine() {
        int seade_number = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { seade_number = INDEX; break; }
        }
        if (seade_number < 0) return false;
        int vaikeväärtus = 설정읽기(seade_number, 0x10);
        if ((vaikeväärtus & 1) == 0 || (vaikeväärtus & 0xfffffffc) < 0x100 || (vaikeväärtus & 0xfffffffc) > 65535) return false;
        입출력기준주소 = vaikeväärtus & 0xfffc;
        int Käsk = 설정읽기(seade_number, 4);
        seade_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (seade_number << 11));
        seade_VALUE.입출력짧은수쓰기(0xcfc, Käsk | 5); // I/O 및 bus master Luba_VALUE, PCI Olek_VALUE 비트는 건드리지 않음
        seade_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!lähtesta_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) seade_ADDRESS[INDEX] = seade_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean lähtesta_VALUE() {
        seade_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Käivita_2 = seade_VALUE.밀리초();
        while ((seade_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (seade_VALUE.밀리초() - Käivita_2 > 100) return false;
        saama_ametikoht = 0; 송신칸 = 0;
        seade_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, seade_VALUE.võrk_Mälu());
        for (int INDEX = 0; INDEX < 4; INDEX++) seade_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, seade_VALUE.võrk_Mälu() + 12288);
        seade_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        seade_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        seade_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        seade_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/levi_VALUE, wrap 연속 salv_VALUE, 8KiB
        seade_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int saatma(int[] andmed, int 길이) {
        if (입출력기준주소 == 0) return -19;
        if (길이 < 14 || 길이 > 1514) return -90;
        int olek_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Käivita_2 = seade_VALUE.밀리초();
        while ((seade_VALUE.입출력정수읽기(olek_port) & 0x2000) == 0)
            if (seade_VALUE.밀리초() - Käivita_2 > 100) return -110;
        int Suurus = 길이 < 60 ? 60 : 길이;
        for (int INDEX = 0; INDEX < Suurus; INDEX++)
            seade_VALUE.kirjutamine_Mälu(seade_VALUE.võrk_Mälu() + 12288 + INDEX, INDEX < 길이 ? andmed[INDEX] : 0);
        seade_VALUE.입출력정수쓰기(olek_port, Suurus | 0x00080000);
        Käivita_2 = seade_VALUE.밀리초();
        while ((seade_VALUE.입출력정수읽기(olek_port) & 0xe0008000) == 0)
            if (seade_VALUE.밀리초() - Käivita_2 > 100) return -110;
        if ((seade_VALUE.입출력정수읽기(olek_port) & 0x8000) == 0) { tõrge_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return 길이;
    }

    static int saama(int[] andmed) {
        if (입출력기준주소 == 0) return 0;
        if ((seade_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            tõrge_COUNT++;
            if (!lähtesta_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((seade_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = seade_VALUE.võrk_Mälu() + saama_ametikoht;
        int Olek_VALUE = 실행관리.짧은수(머리), Suurus = 실행관리.짧은수(머리 + 2);
        if (Suurus == 0xfff0) return 0; // DMA 진행 중
        if (Suurus < 4 || Suurus > 1518) {
            tõrge_COUNT++;
            if (!lähtesta_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int 길이 = Suurus - 4;
        if ((Olek_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < 길이; INDEX++) andmed[INDEX] = seade_VALUE.기억읽기(머리 + 4 + INDEX);
            saama_COUNT++;
        } else { 길이 = 0; tõrge_COUNT++; }
        saama_ametikoht = (saama_ametikoht + Suurus + 4 + 3) & ~3;
        saama_ametikoht &= 8191;
        seade_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (saama_ametikoht - 16) & 65535);
        seade_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return 길이;
    }
}
