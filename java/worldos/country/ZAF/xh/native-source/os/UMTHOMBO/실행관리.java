// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Funda 전용 ukwenza_umyalelo 묶음의 ELF32 qinisekisa, 인수 dlulisa_ixabiso, 한 번에 한 umsebenzisi Inkqubo_ixabiso ukwenza_umyalelo. */
public final class 실행관리 {
    static final int qala_umsebenzisi_inkqubo = 0x04000000;
    static final int umsebenzisi_phela = 0x04400000;
    static final int umfanekiso_phela_idilesi = 0x04200000;
    static final int isiniki_myalelo_qala = 0x04300000;
    static int 인수수 = 0;
    static int[] isiniki_myalelo_idilesi = new int[16];

    static boolean ikliphu(int idilesi, int ubude_ixabiso) {
        return idilesi >= qala_umsebenzisi_inkqubo && idilesi < umsebenzisi_phela && ubude_ixabiso >= 0 && ubude_ixabiso <= umsebenzisi_phela - idilesi;
    }

    static int 수(int idilesi) { return 기억공간.ingcaciso_yegama_inani_elipheleleyo(idilesi); }
    static int 짧은수(int idilesi) { return isixhobo_ixabiso.기억읽기(idilesi) | isixhobo_ixabiso.기억읽기(idilesi + 1) << 8; }
    static void 수쓰기(int idilesi, int ixabiso) {
        for (int indeksa = 0; indeksa < 4; indeksa++) isixhobo_ixabiso.bhala_imemori(idilesi + indeksa, ixabiso >>> (indeksa * 8));
    }

    static int 묶음개수() {
        int idilesi = isixhobo_ixabiso.실행묶음();
        int Ubukhulu = isixhobo_ixabiso.실행묶음크기();
        if (Ubukhulu < 8 || 수(idilesi) != 0x50414b4a) return 0;
        int 개수 = 수(idilesi + 4);
        return 개수 >= 0 && 개수 <= 32 && 개수 <= (Ubukhulu - 8) / 24 ? 개수 : 0;
    }

    static void ufako_nkcukacha_uludwe() {
        for (int indeksa = 0; indeksa < 묶음개수(); indeksa++) {
            int ufako_nkcukacha_ixabiso = isixhobo_ixabiso.실행묶음() + 8 + indeksa * 24;
            for (int ikharakhtha_ixabiso = 0; ikharakhtha_ixabiso < 16 && isixhobo_ixabiso.기억읽기(ufako_nkcukacha_ixabiso + ikharakhtha_ixabiso) != 0; ikharakhtha_ixabiso++)
                문자단말.문자(isixhobo_ixabiso.기억읽기(ufako_nkcukacha_ixabiso + ikharakhtha_ixabiso));
            문자단말.Bhala("\n");
        }
    }

    static int fumana_ufako_nkcukacha(int[] 입력, int Phumeza, int ubude_ixabiso) {
        if (ubude_ixabiso <= 0 || ubude_ixabiso >= 16) return 0;
        for (int indeksa = 0; indeksa < 묶음개수(); indeksa++) {
            int ufako_nkcukacha_ixabiso = isixhobo_ixabiso.실행묶음() + 8 + indeksa * 24;
            boolean 같음 = isixhobo_ixabiso.기억읽기(ufako_nkcukacha_ixabiso + ubude_ixabiso) == 0;
            for (int ikharakhtha_ixabiso = 0; ikharakhtha_ixabiso < ubude_ixabiso; ikharakhtha_ixabiso++)
                if (입력[Phumeza + ikharakhtha_ixabiso] != isixhobo_ixabiso.기억읽기(ufako_nkcukacha_ixabiso + ikharakhtha_ixabiso)) 같음 = false;
            if (같음) return ufako_nkcukacha_ixabiso;
        }
        return 0;
    }

    static int qinisekisa(int iFayili, int ubude_ixabiso) {
        if (ubude_ixabiso < 52 || 수(iFayili) != 0x464c457f || isixhobo_ixabiso.기억읽기(iFayili + 4) != 1
            || isixhobo_ixabiso.기억읽기(iFayili + 5) != 1 || isixhobo_ixabiso.기억읽기(iFayili + 6) != 1
            || 짧은수(iFayili + 16) != 2 || 짧은수(iFayili + 18) != 3 || 수(iFayili + 20) != 1
            || 짧은수(iFayili + 40) != 52 || 짧은수(iFayili + 42) != 32) return -8;
        int ufako_nkcukacha_inqaku_ixabiso = 수(iFayili + 24);
        int 표위치 = 수(iFayili + 28);
        int 개수 = 짧은수(iFayili + 44);
        if (개수 == 0 || 개수 > 16 || 표위치 < 52 || 표위치 > ubude_ixabiso - 개수 * 32) return -8;
        boolean 실행가능 = false;
        for (int indeksa = 0; indeksa < 개수; indeksa++) {
            int 표 = iFayili + 표위치 + indeksa * 32;
            int 종류 = 수(표);
            if (종류 == 2 || 종류 == 3) return -8; // 동적 Nxulumanisa/해석기 미지원
            if (종류 != 1) continue;
            int 위치 = 수(표 + 4), idilesi = 수(표 + 8), ifayile_isayizi = 수(표 + 16), imemori_isayizi = 수(표 + 20);
            int lungelelanisa_ixabiso = 수(표 + 28);
            if (idilesi < qala_umsebenzisi_inkqubo || idilesi >= umfanekiso_phela_idilesi || imemori_isayizi < 0 || imemori_isayizi > umfanekiso_phela_idilesi - idilesi
                || ifayile_isayizi < 0 || ifayile_isayizi > imemori_isayizi || 위치 < 0 || (ifayile_isayizi > 0 && 위치 > ubude_ixabiso - ifayile_isayizi)
                || (lungelelanisa_ixabiso != 0 && (lungelelanisa_ixabiso < 0 || (lungelelanisa_ixabiso & (lungelelanisa_ixabiso - 1)) != 0
                    || ((idilesi - 위치) & (lungelelanisa_ixabiso - 1)) != 0))) return -8;
            for (int 앞 = 0; 앞 < indeksa; 앞++) {
                int 이전 = iFayili + 표위치 + 앞 * 32;
                if (수(이전) == 1 && imemori_isayizi > 0 && 수(이전 + 20) > 0
                    && idilesi < 수(이전 + 8) + 수(이전 + 20) && 수(이전 + 8) < idilesi + imemori_isayizi) return -8;
            }
            if ((수(표 + 24) & 1) != 0 && ufako_nkcukacha_inqaku_ixabiso >= idilesi && ufako_nkcukacha_inqaku_ixabiso - idilesi < ifayile_isayizi) 실행가능 = true;
        }
        return 실행가능 ? ufako_nkcukacha_inqaku_ixabiso : -8;
    }

    static int ukwenza_umyalelo(int[] 입력, int Phumeza, int ubude_ixabiso) {
        while (Phumeza < ubude_ixabiso && 입력[Phumeza] == ' ') Phumeza++;
        int 끝 = Phumeza;
        while (끝 < ubude_ixabiso && 입력[끝] != ' ') 끝++;
        int ufako_nkcukacha_ixabiso = fumana_ufako_nkcukacha(입력, Phumeza, 끝 - Phumeza);
        if (ufako_nkcukacha_ixabiso == 0) return -2;
        int 위치 = 수(ufako_nkcukacha_ixabiso + 16), Ubukhulu = 수(ufako_nkcukacha_ixabiso + 20);
        if (위치 < 8 + 묶음개수() * 24 || Ubukhulu < 52 || 위치 > isixhobo_ixabiso.실행묶음크기() - Ubukhulu) return -8;
        int iFayili = isixhobo_ixabiso.실행묶음() + 위치;
        int ufako_nkcukacha_inqaku_ixabiso = qinisekisa(iFayili, Ubukhulu);
        if (ufako_nkcukacha_inqaku_ixabiso < 0) return ufako_nkcukacha_inqaku_ixabiso;
        isixhobo_ixabiso.umsebenzisi_susa_i_TOC();
        int 표위치 = 수(iFayili + 28), 개수 = 짧은수(iFayili + 44);
        for (int indeksa = 0; indeksa < 개수; indeksa++) {
            int 표 = iFayili + 표위치 + indeksa * 32;
            if (수(표) != 1) continue;
            int 원본 = iFayili + 수(표 + 4), indawo_ekuyiwa_kuyo_ixabiso = 수(표 + 8), ifayile_isayizi = 수(표 + 16);
            for (int ibhayithi_ixabiso = 0; ibhayithi_ixabiso < ifayile_isayizi; ibhayithi_ixabiso++) isixhobo_ixabiso.bhala_imemori(indawo_ekuyiwa_kuyo_ixabiso + ibhayithi_ixabiso, isixhobo_ixabiso.기억읽기(원본 + ibhayithi_ixabiso));
        }
        인수수 = 0;
        int Store_ixabiso = isiniki_myalelo_qala;
        while (끝 < ubude_ixabiso) {
            while (끝 < ubude_ixabiso && 입력[끝] == ' ') 끝++;
            if (끝 == ubude_ixabiso) break;
            if (인수수 == isiniki_myalelo_idilesi.length) return -22;
            Phumeza = 끝;
            while (끝 < ubude_ixabiso && 입력[끝] != ' ') 끝++;
            isiniki_myalelo_idilesi[인수수++] = Store_ixabiso;
            수쓰기(Store_ixabiso, 끝 - Phumeza);
            for (int ikharakhtha_ixabiso = Phumeza; ikharakhtha_ixabiso < 끝; ikharakhtha_ixabiso++) 수쓰기(Store_ixabiso + 4 + (ikharakhtha_ixabiso - Phumeza) * 4, 입력[ikharakhtha_ixabiso]);
            Store_ixabiso += 4 + (끝 - Phumeza) * 4;
        }
        Inethiwekhi_fumba.과정정리();
        파일서술자관리.qala_Inkqubo();
        int 결과 = isixhobo_ixabiso.i_run_umsebenzisi_inkqubo(ufako_nkcukacha_inqaku_ixabiso, umsebenzisi_phela - 16);
        파일서술자관리.과정정리();
        Inethiwekhi_fumba.과정정리();
        return 결과;
    }
}
