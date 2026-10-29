// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_ixabiso fomatha_ixabiso. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] ifayile_itheyibhile = new int[1024];
    static int 바이트해시(int ixabiso, int iingcombolo) { return (ixabiso ^ iingcombolo) * 16777619; }
    static void susa_iingcombolo() {
        for (int indeksa = 0; indeksa < 512; indeksa++) Ugcino_isixhobo_uqhagamshelo.icandelo_iingcombolo[indeksa] = 0;
    }
    static int itheyibhile_inani_elipheleleyo(int 위치) {
        return ifayile_itheyibhile[위치] | ifayile_itheyibhile[위치 + 1] << 8 | ifayile_itheyibhile[위치 + 2] << 16 | ifayile_itheyibhile[위치 + 3] << 24;
    }
    static void bhala_itheyibhile_inani_elipheleleyo(int 위치, int ixabiso) {
        for (int indeksa = 0; indeksa < 4; indeksa++) ifayile_itheyibhile[위치 + indeksa] = (ixabiso >>> (indeksa * 8)) & 255;
    }
    static boolean jonga_itheyibhile() {
        for (int iFayili = 0; iFayili < 8; iFayili++) {
            int ubude_ixabiso = 0;
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 64; isithuba_ufako_nkcukacha++) imemori_uhlobo_loseto_lwefayile.Igama[isithuba_ufako_nkcukacha] = ifayile_itheyibhile[iFayili * 72 + isithuba_ufako_nkcukacha];
            while (ubude_ixabiso < 64 && imemori_uhlobo_loseto_lwefayile.Igama[ubude_ixabiso] != 0) ubude_ixabiso++;
            if (ubude_ixabiso == 0) continue;
            if (!imemori_uhlobo_loseto_lwefayile.jonga_igama(imemori_uhlobo_loseto_lwefayile.Igama, ubude_ixabiso)
                || itheyibhile_inani_elipheleleyo(iFayili * 72 + 64) < 0 || itheyibhile_inani_elipheleleyo(iFayili * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < iFayili; 앞++) {
                boolean 같음 = ifayile_itheyibhile[앞 * 72 + ubude_ixabiso] == 0;
                for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < ubude_ixabiso; isithuba_ufako_nkcukacha++) if (ifayile_itheyibhile[앞 * 72 + isithuba_ufako_nkcukacha] != imemori_uhlobo_loseto_lwefayile.Igama[isithuba_ufako_nkcukacha]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int qala_icandelo = 1 + 보존본 * 259;
        if (Ugcino_isixhobo_uqhagamshelo.Funda(qala_icandelo) < 0 || Ugcino_isixhobo_uqhagamshelo.ingcaciso_yegama_inani_elipheleleyo(0) != 0x4a4b534e) return -1;
        int 세대 = Ugcino_isixhobo_uqhagamshelo.ingcaciso_yegama_inani_elipheleleyo(4), 검사합 = Ugcino_isixhobo_uqhagamshelo.ingcaciso_yegama_inani_elipheleleyo(8);
        if (세대 < 1 || Ugcino_isixhobo_uqhagamshelo.ingcaciso_yegama_inani_elipheleleyo(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int i_hash_ifayile = 0x811c9dc5;
        for (int icandelo_ixabiso = 0; icandelo_ixabiso < 258; icandelo_ixabiso++) {
            if (Ugcino_isixhobo_uqhagamshelo.Funda(qala_icandelo + 1 + icandelo_ixabiso) < 0) return -1;
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 512; isithuba_ufako_nkcukacha++) {
                int ixabiso = Ugcino_isixhobo_uqhagamshelo.icandelo_iingcombolo[isithuba_ufako_nkcukacha];
                i_hash_ifayile = 바이트해시(i_hash_ifayile, ixabiso);
                if (icandelo_ixabiso < 2) ifayile_itheyibhile[icandelo_ixabiso * 512 + isithuba_ufako_nkcukacha] = ixabiso;
            }
        }
        return i_hash_ifayile == 검사합 && jonga_itheyibhile() ? 세대 : -1;
    }
    static int Faka(int 보존본) {
        int qala_icandelo = 1 + 보존본 * 259;
        for (int icandelo_ixabiso = 0; icandelo_ixabiso < 2; icandelo_ixabiso++) {
            if (Ugcino_isixhobo_uqhagamshelo.Funda(qala_icandelo + 1 + icandelo_ixabiso) < 0) return -5;
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 512; isithuba_ufako_nkcukacha++) ifayile_itheyibhile[icandelo_ixabiso * 512 + isithuba_ufako_nkcukacha] = Ugcino_isixhobo_uqhagamshelo.icandelo_iingcombolo[isithuba_ufako_nkcukacha];
        }
        for (int iFayili = 0; iFayili < 8; iFayili++) {
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 64; isithuba_ufako_nkcukacha++) imemori_uhlobo_loseto_lwefayile.이름들[iFayili * 64 + isithuba_ufako_nkcukacha] = ifayile_itheyibhile[iFayili * 72 + isithuba_ufako_nkcukacha];
            imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili] = ifayile_itheyibhile[iFayili * 72] == 0 ? 0 : itheyibhile_inani_elipheleleyo(iFayili * 72 + 64);
            imemori_uhlobo_loseto_lwefayile.허가들[iFayili] = itheyibhile_inani_elipheleleyo(iFayili * 72 + 68) & 511;
            for (int icandelo_ixabiso = 0; icandelo_ixabiso < 32; icandelo_ixabiso++) {
                if (Ugcino_isixhobo_uqhagamshelo.Funda(qala_icandelo + 3 + iFayili * 32 + icandelo_ixabiso) < 0) return -5;
                int idilesi = isixhobo_ixabiso.ifayile_imemori() + iFayili * 16384 + icandelo_ixabiso * 512;
                for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 512; isithuba_ufako_nkcukacha++) isixhobo_ixabiso.bhala_imemori(idilesi + isithuba_ufako_nkcukacha, Ugcino_isixhobo_uqhagamshelo.icandelo_iingcombolo[isithuba_ufako_nkcukacha]);
            }
        }
        return 0;
    }
    static void lungisa() {
        if (Ugcino_isixhobo_uqhagamshelo.Funda(0) < 0 || Ugcino_isixhobo_uqhagamshelo.ingcaciso_yegama_inani_elipheleleyo(0) != 0x54534b4a
            || Ugcino_isixhobo_uqhagamshelo.ingcaciso_yegama_inani_elipheleleyo(4) != 0x3145524f || Ugcino_isixhobo_uqhagamshelo.ingcaciso_yegama_inani_elipheleleyo(8) != 2048
            || Ugcino_isixhobo_uqhagamshelo.ingcaciso_yegama_inani_elipheleleyo(12) != 0x3153464a) {
            문자단말.Bhala("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Ugcino_isixhobo_uqhagamshelo.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.Bhala("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Faka(현재보존본) < 0) {
            문자단말.Bhala("STORE read failed; halted to preserve files\n"); isixhobo_ixabiso.정지();
        }
        문자단말.Bhala("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int ngqamanisa() {
        if (!Ugcino_isixhobo_uqhagamshelo.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, qala_icandelo = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 isixhobo_ixabiso 캐시를 비운다.
        susa_iingcombolo();
        if (Ugcino_isixhobo_uqhagamshelo.Bhala(qala_icandelo) < 0 || Ugcino_isixhobo_uqhagamshelo.밀어쓰기() < 0) return -5;
        for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 1024; isithuba_ufako_nkcukacha++) ifayile_itheyibhile[isithuba_ufako_nkcukacha] = 0;
        for (int iFayili = 0; iFayili < 8; iFayili++) if (imemori_uhlobo_loseto_lwefayile.이름들[iFayili * 64] != 0) {
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 64; isithuba_ufako_nkcukacha++) ifayile_itheyibhile[iFayili * 72 + isithuba_ufako_nkcukacha] = imemori_uhlobo_loseto_lwefayile.이름들[iFayili * 64 + isithuba_ufako_nkcukacha];
            bhala_itheyibhile_inani_elipheleleyo(iFayili * 72 + 64, imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili]);
            bhala_itheyibhile_inani_elipheleleyo(iFayili * 72 + 68, imemori_uhlobo_loseto_lwefayile.허가들[iFayili]);
        }
        int i_hash_ifayile = 0x811c9dc5;
        for (int icandelo_ixabiso = 0; icandelo_ixabiso < 258; icandelo_ixabiso++) {
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 512; isithuba_ufako_nkcukacha++) {
                int ixabiso = 0;
                if (icandelo_ixabiso < 2) ixabiso = ifayile_itheyibhile[icandelo_ixabiso * 512 + isithuba_ufako_nkcukacha];
                else {
                    int iFayili = (icandelo_ixabiso - 2) / 32, 위치 = (icandelo_ixabiso - 2) % 32 * 512 + isithuba_ufako_nkcukacha;
                    if (ifayile_itheyibhile[iFayili * 72] != 0 && 위치 < imemori_uhlobo_loseto_lwefayile.isayizi_uludwe[iFayili])
                        ixabiso = isixhobo_ixabiso.기억읽기(isixhobo_ixabiso.ifayile_imemori() + iFayili * 16384 + 위치);
                }
                Ugcino_isixhobo_uqhagamshelo.icandelo_iingcombolo[isithuba_ufako_nkcukacha] = ixabiso; i_hash_ifayile = 바이트해시(i_hash_ifayile, ixabiso);
            }
            if (Ugcino_isixhobo_uqhagamshelo.Bhala(qala_icandelo + 1 + icandelo_ixabiso) < 0) return -5;
        }
        if (Ugcino_isixhobo_uqhagamshelo.밀어쓰기() < 0) return -5;
        susa_iingcombolo(); Ugcino_isixhobo_uqhagamshelo.bhala_inani_elipheleleyo_ixabiso(0, 0x4a4b534e);
        Ugcino_isixhobo_uqhagamshelo.bhala_inani_elipheleleyo_ixabiso(4, 세대번호 + 1); Ugcino_isixhobo_uqhagamshelo.bhala_inani_elipheleleyo_ixabiso(8, i_hash_ifayile);
        Ugcino_isixhobo_uqhagamshelo.bhala_inani_elipheleleyo_ixabiso(12, (세대번호 + 1) ^ i_hash_ifayile ^ 0x4a4b534e);
        if (Ugcino_isixhobo_uqhagamshelo.Bhala(qala_icandelo) < 0 || Ugcino_isixhobo_uqhagamshelo.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
