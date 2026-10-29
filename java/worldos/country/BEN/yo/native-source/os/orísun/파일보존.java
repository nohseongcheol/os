// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_iye ìgúnrégé_iye. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] fáìlì_atọ́ka = new int[1024];
    static int 바이트해시(int iye, int détà) { return (iye ^ détà) * 16777619; }
    static void mú_kúrò_détà() {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 512; wá_atọ̀ka_àkóónú++) Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.abala_détà[wá_atọ̀ka_àkóónú] = 0;
    }
    static int atọ́ka_nọ́ńbà_odindi(int 위치) {
        return fáìlì_atọ́ka[위치] | fáìlì_atọ́ka[위치 + 1] << 8 | fáìlì_atọ́ka[위치 + 2] << 16 | fáìlì_atọ́ka[위치 + 3] << 24;
    }
    static void kọ_atọ́ka_nọ́ńbà_odindi(int 위치, int iye) {
        for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 4; wá_atọ̀ka_àkóónú++) fáìlì_atọ́ka[위치 + wá_atọ̀ka_àkóónú] = (iye >>> (wá_atọ̀ka_àkóónú * 8)) & 255;
    }
    static boolean ṣàyẹ̀wò_atọ́ka() {
        for (int Fáìlì = 0; Fáìlì < 8; Fáìlì++) {
            int gígùn_iye = 0;
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 64; ààyè_ìfàyọkàsí_ìgbéwọlé++) ibi_ìpamọ́_ìlànà_ètò_fáìlì.Orúkọ[ààyè_ìfàyọkàsí_ìgbéwọlé] = fáìlì_atọ́ka[Fáìlì * 72 + ààyè_ìfàyọkàsí_ìgbéwọlé];
            while (gígùn_iye < 64 && ibi_ìpamọ́_ìlànà_ètò_fáìlì.Orúkọ[gígùn_iye] != 0) gígùn_iye++;
            if (gígùn_iye == 0) continue;
            if (!ibi_ìpamọ́_ìlànà_ètò_fáìlì.ṣàyẹ̀wò_orúkọ(ibi_ìpamọ́_ìlànà_ètò_fáìlì.Orúkọ, gígùn_iye)
                || atọ́ka_nọ́ńbà_odindi(Fáìlì * 72 + 64) < 0 || atọ́ka_nọ́ńbà_odindi(Fáìlì * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Fáìlì; 앞++) {
                boolean 같음 = fáìlì_atọ́ka[앞 * 72 + gígùn_iye] == 0;
                for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < gígùn_iye; ààyè_ìfàyọkàsí_ìgbéwọlé++) if (fáìlì_atọ́ka[앞 * 72 + ààyè_ìfàyọkàsí_ìgbéwọlé] != ibi_ìpamọ́_ìlànà_ètò_fáìlì.Orúkọ[ààyè_ìfàyọkàsí_ìgbéwọlé]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int bẹ̀rẹ̀_abala = 1 + 보존본 * 259;
        if (Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.Kàá(bẹ̀rẹ̀_abala) < 0 || Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(0) != 0x4a4b534e) return -1;
        int 세대 = Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(4), 검사합 = Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(8);
        if (세대 < 1 || Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int burú_fáìlì = 0x811c9dc5;
        for (int abala_iye = 0; abala_iye < 258; abala_iye++) {
            if (Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.Kàá(bẹ̀rẹ̀_abala + 1 + abala_iye) < 0) return -1;
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 512; ààyè_ìfàyọkàsí_ìgbéwọlé++) {
                int iye = Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.abala_détà[ààyè_ìfàyọkàsí_ìgbéwọlé];
                burú_fáìlì = 바이트해시(burú_fáìlì, iye);
                if (abala_iye < 2) fáìlì_atọ́ka[abala_iye * 512 + ààyè_ìfàyọkàsí_ìgbéwọlé] = iye;
            }
        }
        return burú_fáìlì == 검사합 && ṣàyẹ̀wò_atọ́ka() ? 세대 : -1;
    }
    static int ki(int 보존본) {
        int bẹ̀rẹ̀_abala = 1 + 보존본 * 259;
        for (int abala_iye = 0; abala_iye < 2; abala_iye++) {
            if (Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.Kàá(bẹ̀rẹ̀_abala + 1 + abala_iye) < 0) return -5;
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 512; ààyè_ìfàyọkàsí_ìgbéwọlé++) fáìlì_atọ́ka[abala_iye * 512 + ààyè_ìfàyọkàsí_ìgbéwọlé] = Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.abala_détà[ààyè_ìfàyọkàsí_ìgbéwọlé];
        }
        for (int Fáìlì = 0; Fáìlì < 8; Fáìlì++) {
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 64; ààyè_ìfàyọkàsí_ìgbéwọlé++) ibi_ìpamọ́_ìlànà_ètò_fáìlì.이름들[Fáìlì * 64 + ààyè_ìfàyọkàsí_ìgbéwọlé] = fáìlì_atọ́ka[Fáìlì * 72 + ààyè_ìfàyọkàsí_ìgbéwọlé];
            ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì] = fáìlì_atọ́ka[Fáìlì * 72] == 0 ? 0 : atọ́ka_nọ́ńbà_odindi(Fáìlì * 72 + 64);
            ibi_ìpamọ́_ìlànà_ètò_fáìlì.허가들[Fáìlì] = atọ́ka_nọ́ńbà_odindi(Fáìlì * 72 + 68) & 511;
            for (int abala_iye = 0; abala_iye < 32; abala_iye++) {
                if (Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.Kàá(bẹ̀rẹ̀_abala + 3 + Fáìlì * 32 + abala_iye) < 0) return -5;
                int àdírẹ́ẹ̀sì = ohun_èlò_iye.fáìlì_ibi_ìpamọ́() + Fáìlì * 16384 + abala_iye * 512;
                for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 512; ààyè_ìfàyọkàsí_ìgbéwọlé++) ohun_èlò_iye.kọ_ibi_ìpamọ́(àdírẹ́ẹ̀sì + ààyè_ìfàyọkàsí_ìgbéwọlé, Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.abala_détà[ààyè_ìfàyọkàsí_ìgbéwọlé]);
            }
        }
        return 0;
    }
    static void gbaradì() {
        if (Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.Kàá(0) < 0 || Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(0) != 0x54534b4a
            || Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(4) != 0x3145524f || Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(8) != 2048
            || Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(12) != 0x3153464a) {
            문자단말.Kọ("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.Kọ("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (ki(현재보존본) < 0) {
            문자단말.Kọ("STORE read failed; halted to preserve files\n"); ohun_èlò_iye.정지();
        }
        문자단말.Kọ("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int múdọ́gba() {
        if (!Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, bẹ̀rẹ̀_abala = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 ohun_èlò_iye 캐시를 비운다.
        mú_kúrò_détà();
        if (Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.Kọ(bẹ̀rẹ̀_abala) < 0 || Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.밀어쓰기() < 0) return -5;
        for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 1024; ààyè_ìfàyọkàsí_ìgbéwọlé++) fáìlì_atọ́ka[ààyè_ìfàyọkàsí_ìgbéwọlé] = 0;
        for (int Fáìlì = 0; Fáìlì < 8; Fáìlì++) if (ibi_ìpamọ́_ìlànà_ètò_fáìlì.이름들[Fáìlì * 64] != 0) {
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 64; ààyè_ìfàyọkàsí_ìgbéwọlé++) fáìlì_atọ́ka[Fáìlì * 72 + ààyè_ìfàyọkàsí_ìgbéwọlé] = ibi_ìpamọ́_ìlànà_ètò_fáìlì.이름들[Fáìlì * 64 + ààyè_ìfàyọkàsí_ìgbéwọlé];
            kọ_atọ́ka_nọ́ńbà_odindi(Fáìlì * 72 + 64, ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì]);
            kọ_atọ́ka_nọ́ńbà_odindi(Fáìlì * 72 + 68, ibi_ìpamọ́_ìlànà_ètò_fáìlì.허가들[Fáìlì]);
        }
        int burú_fáìlì = 0x811c9dc5;
        for (int abala_iye = 0; abala_iye < 258; abala_iye++) {
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 512; ààyè_ìfàyọkàsí_ìgbéwọlé++) {
                int iye = 0;
                if (abala_iye < 2) iye = fáìlì_atọ́ka[abala_iye * 512 + ààyè_ìfàyọkàsí_ìgbéwọlé];
                else {
                    int Fáìlì = (abala_iye - 2) / 32, 위치 = (abala_iye - 2) % 32 * 512 + ààyè_ìfàyọkàsí_ìgbéwọlé;
                    if (fáìlì_atọ́ka[Fáìlì * 72] != 0 && 위치 < ibi_ìpamọ́_ìlànà_ètò_fáìlì.ìwọn_Àtòkọ[Fáìlì])
                        iye = ohun_èlò_iye.기억읽기(ohun_èlò_iye.fáìlì_ibi_ìpamọ́() + Fáìlì * 16384 + 위치);
                }
                Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.abala_détà[ààyè_ìfàyọkàsí_ìgbéwọlé] = iye; burú_fáìlì = 바이트해시(burú_fáìlì, iye);
            }
            if (Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.Kọ(bẹ̀rẹ̀_abala + 1 + abala_iye) < 0) return -5;
        }
        if (Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.밀어쓰기() < 0) return -5;
        mú_kúrò_détà(); Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.kọ_nọ́ńbà_odindi_iye(0, 0x4a4b534e);
        Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.kọ_nọ́ńbà_odindi_iye(4, 세대번호 + 1); Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.kọ_nọ́ńbà_odindi_iye(8, burú_fáìlì);
        Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.kọ_nọ́ńbà_odindi_iye(12, (세대번호 + 1) ^ burú_fáìlì ^ 0x4a4b534e);
        if (Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.Kọ(bẹ̀rẹ̀_abala) < 0 || Ibi_ìpamọ́_ohun_èlò_Ìsomọ́.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
