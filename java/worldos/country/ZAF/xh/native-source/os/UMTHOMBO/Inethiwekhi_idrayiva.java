// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 thumela_ixabiso 버퍼와 8KiB 수신 iluphu_ixabiso. 인터럽트 대신 폴링한다. */
public final class Inethiwekhi_idrayiva {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] isixhobo_idilesi = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        isixhobo_ixabiso.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return isixhobo_ixabiso.입출력정수읽기(0xcfc);
    }

    static boolean lungisa() {
        int 장치번호 = -1;
        for (int indeksa = 0; indeksa < 32; indeksa++) {
            if (설정읽기(indeksa, 0) == 0x813910ec) { 장치번호 = indeksa; break; }
        }
        if (장치번호 < 0) return false;
        int ixabiso_elisisiseko = 설정읽기(장치번호, 0x10);
        if ((ixabiso_elisisiseko & 1) == 0 || (ixabiso_elisisiseko & 0xfffffffc) < 0x100 || (ixabiso_elisisiseko & 0xfffffffc) > 65535) return false;
        입출력기준주소 = ixabiso_elisisiseko & 0xfffc;
        int Umyalelo = 설정읽기(장치번호, 4);
        isixhobo_ixabiso.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        isixhobo_ixabiso.입출력짧은수쓰기(0xcfc, Umyalelo | 5); // I/O 및 bus master vumela_ixabiso, PCI imo_ixabiso 비트는 건드리지 않음
        isixhobo_ixabiso.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!seta_kwakhona_ixabiso()) { 입출력기준주소 = 0; return false; }
        for (int indeksa = 0; indeksa < 6; indeksa++) isixhobo_idilesi[indeksa] = isixhobo_ixabiso.입출력바이트읽기(입출력기준주소 + indeksa);
        return true;
    }

    static boolean seta_kwakhona_ixabiso() {
        isixhobo_ixabiso.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Phumeza = isixhobo_ixabiso.밀리초();
        while ((isixhobo_ixabiso.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (isixhobo_ixabiso.밀리초() - Phumeza > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        isixhobo_ixabiso.입출력정수쓰기(입출력기준주소 + 0x30, isixhobo_ixabiso.Inethiwekhi_imemori());
        for (int indeksa = 0; indeksa < 4; indeksa++) isixhobo_ixabiso.입출력정수쓰기(입출력기준주소 + 0x20 + indeksa * 4, isixhobo_ixabiso.Inethiwekhi_imemori() + 12288);
        isixhobo_ixabiso.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        isixhobo_ixabiso.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        isixhobo_ixabiso.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        isixhobo_ixabiso.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/usasazo_ixabiso, wrap 연속 Store_ixabiso, 8KiB
        isixhobo_ixabiso.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int thumela(int[] iingcombolo, int ubude_ixabiso) {
        if (입출력기준주소 == 0) return -19;
        if (ubude_ixabiso < 14 || ubude_ixabiso > 1514) return -90;
        int imo_iphothi = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Phumeza = isixhobo_ixabiso.밀리초();
        while ((isixhobo_ixabiso.입출력정수읽기(imo_iphothi) & 0x2000) == 0)
            if (isixhobo_ixabiso.밀리초() - Phumeza > 100) return -110;
        int Ubukhulu = ubude_ixabiso < 60 ? 60 : ubude_ixabiso;
        for (int indeksa = 0; indeksa < Ubukhulu; indeksa++)
            isixhobo_ixabiso.bhala_imemori(isixhobo_ixabiso.Inethiwekhi_imemori() + 12288 + indeksa, indeksa < ubude_ixabiso ? iingcombolo[indeksa] : 0);
        isixhobo_ixabiso.입출력정수쓰기(imo_iphothi, Ubukhulu | 0x00080000);
        Phumeza = isixhobo_ixabiso.밀리초();
        while ((isixhobo_ixabiso.입출력정수읽기(imo_iphothi) & 0xe0008000) == 0)
            if (isixhobo_ixabiso.밀리초() - Phumeza > 100) return -110;
        if ((isixhobo_ixabiso.입출력정수읽기(imo_iphothi) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return ubude_ixabiso;
    }

    static int 받기(int[] iingcombolo) {
        if (입출력기준주소 == 0) return 0;
        if ((isixhobo_ixabiso.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!seta_kwakhona_ixabiso()) 입출력기준주소 = 0;
            return 0;
        }
        if ((isixhobo_ixabiso.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = isixhobo_ixabiso.Inethiwekhi_imemori() + 수신위치;
        int imo_ixabiso = 실행관리.짧은수(머리), Ubukhulu = 실행관리.짧은수(머리 + 2);
        if (Ubukhulu == 0xfff0) return 0; // DMA 진행 중
        if (Ubukhulu < 4 || Ubukhulu > 1518) {
            오류수++;
            if (!seta_kwakhona_ixabiso()) 입출력기준주소 = 0;
            return 0;
        }
        int ubude_ixabiso = Ubukhulu - 4;
        if ((imo_ixabiso & 1) != 0) {
            for (int indeksa = 0; indeksa < ubude_ixabiso; indeksa++) iingcombolo[indeksa] = isixhobo_ixabiso.기억읽기(머리 + 4 + indeksa);
            수신수++;
        } else { ubude_ixabiso = 0; 오류수++; }
        수신위치 = (수신위치 + Ubukhulu + 4 + 3) & ~3;
        수신위치 &= 8191;
        isixhobo_ixabiso.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        isixhobo_ixabiso.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return ubude_ixabiso;
    }
}
