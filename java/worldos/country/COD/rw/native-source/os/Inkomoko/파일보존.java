// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_agaciro imiterere_agaciro. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] dosiye_imbonerahamwe = new int[1024];
    static int 바이트해시(int agaciro, int amakurushingiro) { return (agaciro ^ amakurushingiro) * 16777619; }
    static void gukuraho_amakurushingiro() {
        for (int umugerekashakiro = 0; umugerekashakiro < 512; umugerekashakiro++) Ububiko_igendanwa_kwihuza.igice_amakurushingiro[umugerekashakiro] = 0;
    }
    static int imbonerahamwe_umubare_wuzuye(int 위치) {
        return dosiye_imbonerahamwe[위치] | dosiye_imbonerahamwe[위치 + 1] << 8 | dosiye_imbonerahamwe[위치 + 2] << 16 | dosiye_imbonerahamwe[위치 + 3] << 24;
    }
    static void kwandika_imbonerahamwe_umubare_wuzuye(int 위치, int agaciro) {
        for (int umugerekashakiro = 0; umugerekashakiro < 4; umugerekashakiro++) dosiye_imbonerahamwe[위치 + umugerekashakiro] = (agaciro >>> (umugerekashakiro * 8)) & 255;
    }
    static boolean sheki_imbonerahamwe() {
        for (int Idosiye = 0; Idosiye < 8; Idosiye++) {
            int uburebure_agaciro = 0;
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 64; umwanya_icyinjizwa++) ububiko_sisitemu_ya_dosiye.Izina[umwanya_icyinjizwa] = dosiye_imbonerahamwe[Idosiye * 72 + umwanya_icyinjizwa];
            while (uburebure_agaciro < 64 && ububiko_sisitemu_ya_dosiye.Izina[uburebure_agaciro] != 0) uburebure_agaciro++;
            if (uburebure_agaciro == 0) continue;
            if (!ububiko_sisitemu_ya_dosiye.sheki_izina(ububiko_sisitemu_ya_dosiye.Izina, uburebure_agaciro)
                || imbonerahamwe_umubare_wuzuye(Idosiye * 72 + 64) < 0 || imbonerahamwe_umubare_wuzuye(Idosiye * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Idosiye; 앞++) {
                boolean 같음 = dosiye_imbonerahamwe[앞 * 72 + uburebure_agaciro] == 0;
                for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < uburebure_agaciro; umwanya_icyinjizwa++) if (dosiye_imbonerahamwe[앞 * 72 + umwanya_icyinjizwa] != ububiko_sisitemu_ya_dosiye.Izina[umwanya_icyinjizwa]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Itangira_igice = 1 + 보존본 * 259;
        if (Ububiko_igendanwa_kwihuza.읽기(Itangira_igice) < 0 || Ububiko_igendanwa_kwihuza.gusesengura_umubare_wuzuye(0) != 0x4a4b534e) return -1;
        int 세대 = Ububiko_igendanwa_kwihuza.gusesengura_umubare_wuzuye(4), 검사합 = Ububiko_igendanwa_kwihuza.gusesengura_umubare_wuzuye(8);
        if (세대 < 1 || Ububiko_igendanwa_kwihuza.gusesengura_umubare_wuzuye(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int hashi_dosiye = 0x811c9dc5;
        for (int igice_agaciro = 0; igice_agaciro < 258; igice_agaciro++) {
            if (Ububiko_igendanwa_kwihuza.읽기(Itangira_igice + 1 + igice_agaciro) < 0) return -1;
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 512; umwanya_icyinjizwa++) {
                int agaciro = Ububiko_igendanwa_kwihuza.igice_amakurushingiro[umwanya_icyinjizwa];
                hashi_dosiye = 바이트해시(hashi_dosiye, agaciro);
                if (igice_agaciro < 2) dosiye_imbonerahamwe[igice_agaciro * 512 + umwanya_icyinjizwa] = agaciro;
            }
        }
        return hashi_dosiye == 검사합 && sheki_imbonerahamwe() ? 세대 : -1;
    }
    static int Ibirimo(int 보존본) {
        int Itangira_igice = 1 + 보존본 * 259;
        for (int igice_agaciro = 0; igice_agaciro < 2; igice_agaciro++) {
            if (Ububiko_igendanwa_kwihuza.읽기(Itangira_igice + 1 + igice_agaciro) < 0) return -5;
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 512; umwanya_icyinjizwa++) dosiye_imbonerahamwe[igice_agaciro * 512 + umwanya_icyinjizwa] = Ububiko_igendanwa_kwihuza.igice_amakurushingiro[umwanya_icyinjizwa];
        }
        for (int Idosiye = 0; Idosiye < 8; Idosiye++) {
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 64; umwanya_icyinjizwa++) ububiko_sisitemu_ya_dosiye.이름들[Idosiye * 64 + umwanya_icyinjizwa] = dosiye_imbonerahamwe[Idosiye * 72 + umwanya_icyinjizwa];
            ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye] = dosiye_imbonerahamwe[Idosiye * 72] == 0 ? 0 : imbonerahamwe_umubare_wuzuye(Idosiye * 72 + 64);
            ububiko_sisitemu_ya_dosiye.허가들[Idosiye] = imbonerahamwe_umubare_wuzuye(Idosiye * 72 + 68) & 511;
            for (int igice_agaciro = 0; igice_agaciro < 32; igice_agaciro++) {
                if (Ububiko_igendanwa_kwihuza.읽기(Itangira_igice + 3 + Idosiye * 32 + igice_agaciro) < 0) return -5;
                int aderesi = igendanwa_agaciro.dosiye_ububiko() + Idosiye * 16384 + igice_agaciro * 512;
                for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 512; umwanya_icyinjizwa++) igendanwa_agaciro.kwandika_ububiko(aderesi + umwanya_icyinjizwa, Ububiko_igendanwa_kwihuza.igice_amakurushingiro[umwanya_icyinjizwa]);
            }
        }
        return 0;
    }
    static void Gutegura() {
        if (Ububiko_igendanwa_kwihuza.읽기(0) < 0 || Ububiko_igendanwa_kwihuza.gusesengura_umubare_wuzuye(0) != 0x54534b4a
            || Ububiko_igendanwa_kwihuza.gusesengura_umubare_wuzuye(4) != 0x3145524f || Ububiko_igendanwa_kwihuza.gusesengura_umubare_wuzuye(8) != 2048
            || Ububiko_igendanwa_kwihuza.gusesengura_umubare_wuzuye(12) != 0x3153464a) {
            문자단말.kwandika("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Ububiko_igendanwa_kwihuza.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.kwandika("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (Ibirimo(현재보존본) < 0) {
            문자단말.kwandika("STORE read failed; halted to preserve files\n"); igendanwa_agaciro.정지();
        }
        문자단말.kwandika("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int guhuza() {
        if (!Ububiko_igendanwa_kwihuza.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, Itangira_igice = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 igendanwa_agaciro 캐시를 비운다.
        gukuraho_amakurushingiro();
        if (Ububiko_igendanwa_kwihuza.kwandika(Itangira_igice) < 0 || Ububiko_igendanwa_kwihuza.밀어쓰기() < 0) return -5;
        for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 1024; umwanya_icyinjizwa++) dosiye_imbonerahamwe[umwanya_icyinjizwa] = 0;
        for (int Idosiye = 0; Idosiye < 8; Idosiye++) if (ububiko_sisitemu_ya_dosiye.이름들[Idosiye * 64] != 0) {
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 64; umwanya_icyinjizwa++) dosiye_imbonerahamwe[Idosiye * 72 + umwanya_icyinjizwa] = ububiko_sisitemu_ya_dosiye.이름들[Idosiye * 64 + umwanya_icyinjizwa];
            kwandika_imbonerahamwe_umubare_wuzuye(Idosiye * 72 + 64, ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye]);
            kwandika_imbonerahamwe_umubare_wuzuye(Idosiye * 72 + 68, ububiko_sisitemu_ya_dosiye.허가들[Idosiye]);
        }
        int hashi_dosiye = 0x811c9dc5;
        for (int igice_agaciro = 0; igice_agaciro < 258; igice_agaciro++) {
            for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 512; umwanya_icyinjizwa++) {
                int agaciro = 0;
                if (igice_agaciro < 2) agaciro = dosiye_imbonerahamwe[igice_agaciro * 512 + umwanya_icyinjizwa];
                else {
                    int Idosiye = (igice_agaciro - 2) / 32, 위치 = (igice_agaciro - 2) % 32 * 512 + umwanya_icyinjizwa;
                    if (dosiye_imbonerahamwe[Idosiye * 72] != 0 && 위치 < ububiko_sisitemu_ya_dosiye.ingano_Urutonde[Idosiye])
                        agaciro = igendanwa_agaciro.기억읽기(igendanwa_agaciro.dosiye_ububiko() + Idosiye * 16384 + 위치);
                }
                Ububiko_igendanwa_kwihuza.igice_amakurushingiro[umwanya_icyinjizwa] = agaciro; hashi_dosiye = 바이트해시(hashi_dosiye, agaciro);
            }
            if (Ububiko_igendanwa_kwihuza.kwandika(Itangira_igice + 1 + igice_agaciro) < 0) return -5;
        }
        if (Ububiko_igendanwa_kwihuza.밀어쓰기() < 0) return -5;
        gukuraho_amakurushingiro(); Ububiko_igendanwa_kwihuza.kwandika_umubare_wuzuye_agaciro(0, 0x4a4b534e);
        Ububiko_igendanwa_kwihuza.kwandika_umubare_wuzuye_agaciro(4, 세대번호 + 1); Ububiko_igendanwa_kwihuza.kwandika_umubare_wuzuye_agaciro(8, hashi_dosiye);
        Ububiko_igendanwa_kwihuza.kwandika_umubare_wuzuye_agaciro(12, (세대번호 + 1) ^ hashi_dosiye ^ 0x4a4b534e);
        if (Ububiko_igendanwa_kwihuza.kwandika(Itangira_igice) < 0 || Ububiko_igendanwa_kwihuza.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
