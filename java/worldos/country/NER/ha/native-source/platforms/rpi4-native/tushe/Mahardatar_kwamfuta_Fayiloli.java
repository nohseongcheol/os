// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fayil 64개, 파일당 16384바이트, 서술자 16개. 모든 Tarin_bayani/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Kuskure 번호다.
 */
public final class Mahardatar_kwamfuta_Fayiloli {
    static final int 파일수 = 64;
    static int[] Suna = new int[파일수 * 64];
    static int[] 이름길이 = new int[파일수];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] kunshiya_Daraja = new int[파일수 * 4096];
    static int[] Tsawo_Daraja = new int[파일수];
    static int[] 참조수 = new int[파일수];
    static int[] 사용 = new int[16];
    static int[] tageti = new int[16];
    static int[] 위치 = new int[16];
    static int[] tsari_yanayin_aiki = new int[16];
    static int[] Hanyar_shiga = new int[64];
    static int Hanyar_shiga_Tsawo;

    public static int 파일한도() { return 파일수; }
    static int 자료읽기(int Fayil, int 자리) { return (kunshiya_Daraja[Fayil * 4096 + 자리 / 4] >>> ((자리 & 3) * 8)) & 255; }
    static void Rubuta_Tarin_bayani(int Fayil, int 자리, int Daraja) {
        int rami_Mashigar_bayanai = Fayil * 4096 + 자리 / 4, Matsar_da_Daraja = (자리 & 3) * 8;
        kunshiya_Daraja[rami_Mashigar_bayanai] = (kunshiya_Daraja[rami_Mashigar_bayanai] & ~(255 << Matsar_da_Daraja)) | ((Daraja & 255) << Matsar_da_Daraja);
    }

    public static int Hanyar_shiga_Fara(int Girma) {
        Hanyar_shiga_Tsawo = 0;
        if (Girma < 1 || Girma > 63) return -36;
        Hanyar_shiga_Tsawo = Girma;
        for (int Warware_Indes = 0; Warware_Indes < Girma; Warware_Indes++) Hanyar_shiga[Warware_Indes] = 0;
        return 0;
    }
    public static int Hanyar_shiga_bayit(int Indes, int Daraja) {
        if (Indes < 0 || Indes >= Hanyar_shiga_Tsawo || Daraja < 1 || Daraja > 255) return -22;
        Hanyar_shiga[Indes] = Daraja; return 0;
    }
    static int nema_Mashigar_bayanai() {
        for (int Fayil_Indes = 0; Fayil_Indes < 파일수; Fayil_Indes++) if (이름길이[Fayil_Indes] > 0 && 이름길이[Fayil_Indes] == 정규길이 && 접두(Suna, Fayil_Indes * 64, 이름길이[Fayil_Indes], 정규, 정규길이)) return Fayil_Indes;
        return -1;
    }
    public static int Buɗe(int 플래그) {
        if (Hanyar_shiga_Tsawo == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Warware_Indes = 0; Warware_Indes < Hanyar_shiga_Tsawo; Warware_Indes++) if (Hanyar_shiga[Warware_Indes] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int 결과 = Gajarta_kimar_bayanai_Daraja(); if (결과 < 0) return 결과;
        if (nema_ma_ajiya(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Fayil = nema_Mashigar_bayanai();
        if (Fayil >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fayil < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Warware_Indes = 0; Warware_Indes < 16; Warware_Indes++) if (사용[Warware_Indes] == 0) { 서술자 = Warware_Indes; break; }
        if (서술자 < 0) return -24;
        if (Fayil < 0) {
            for (int Warware_Indes = 0; Warware_Indes < 파일수; Warware_Indes++) if (이름길이[Warware_Indes] == 0 && 참조수[Warware_Indes] == 0) { Fayil = Warware_Indes; break; }
            if (Fayil < 0) return -28;
            이름길이[Fayil] = 정규길이;
            for (int Warware_Indes = 0; Warware_Indes < 정규길이; Warware_Indes++) Suna[Fayil * 64 + Warware_Indes] = 정규[Warware_Indes];
            Tsawo_Daraja[Fayil] = 0;
        }
        if ((플래그 & 0x200) != 0) Tsawo_Daraja[Fayil] = 0;
        사용[서술자] = 1; tageti[서술자] = Fayil; 위치[서술자] = 0; tsari_yanayin_aiki[서술자] = 플래그;
        참조수[Fayil]++;
        return 서술자 + 3;
    }
    static int Tabbatar_da(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Yi_Karatu(int 서술자) {
        int rami_Mashigar_bayanai = Tabbatar_da(서술자);
        if (rami_Mashigar_bayanai < 0 || (tsari_yanayin_aiki[rami_Mashigar_bayanai] & 3) == 1) return -9;
        int Fayil = tageti[rami_Mashigar_bayanai];
        if (위치[rami_Mashigar_bayanai] >= Tsawo_Daraja[Fayil]) return 256; // EOF와 Na_hakika_Tarin_bayani 0x00..0xff 구별
        return 자료읽기(Fayil, 위치[rami_Mashigar_bayanai]++);
    }
    public static int Yi_Rubutu(int 서술자, int Daraja) {
        int rami_Mashigar_bayanai = Tabbatar_da(서술자);
        if (rami_Mashigar_bayanai < 0 || (tsari_yanayin_aiki[rami_Mashigar_bayanai] & 3) == 0) return -9;
        int Fayil = tageti[rami_Mashigar_bayanai];
        if ((tsari_yanayin_aiki[rami_Mashigar_bayanai] & 0x400) != 0) 위치[rami_Mashigar_bayanai] = Tsawo_Daraja[Fayil];
        if (위치[rami_Mashigar_bayanai] >= 16384) return -28;
        while (Tsawo_Daraja[Fayil] < 위치[rami_Mashigar_bayanai]) Rubuta_Tarin_bayani(Fayil, Tsawo_Daraja[Fayil]++, 0);
        Rubuta_Tarin_bayani(Fayil, 위치[rami_Mashigar_bayanai]++, Daraja);
        if (Tsawo_Daraja[Fayil] < 위치[rami_Mashigar_bayanai]) Tsawo_Daraja[Fayil] = 위치[rami_Mashigar_bayanai];
        return 1;
    }
    public static int 옮기기(int 서술자, int 거리, int 기준) {
        int rami_Mashigar_bayanai = Tabbatar_da(서술자);
        if (rami_Mashigar_bayanai < 0) return -9;
        if (기준 < 0 || 기준 > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (기준 == 0 ? 0 : 기준 == 1 ? 위치[rami_Mashigar_bayanai] : Tsawo_Daraja[tageti[rami_Mashigar_bayanai]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        위치[rami_Mashigar_bayanai] = 새위치; return 새위치;
    }
    public static int Rufe(int 서술자) {
        int rami_Mashigar_bayanai = Tabbatar_da(서술자);
        if (rami_Mashigar_bayanai < 0) return -9;
        참조수[tageti[rami_Mashigar_bayanai]]--; 사용[rami_Mashigar_bayanai] = 0; return 0;
    }
    public static int Girma(int 서술자) {
        int rami_Mashigar_bayanai = Tabbatar_da(서술자); return rami_Mashigar_bayanai < 0 ? -9 : Tsawo_Daraja[tageti[rami_Mashigar_bayanai]];
    }
    public static int zubi_Tsawo(int 서술자, int Girma) {
        int rami_Mashigar_bayanai = Tabbatar_da(서술자);
        if (rami_Mashigar_bayanai < 0 || (tsari_yanayin_aiki[rami_Mashigar_bayanai] & 3) == 0) return -9;
        if (Girma < 0 || Girma > 16384) return -22;
        int Fayil = tageti[rami_Mashigar_bayanai];
        while (Tsawo_Daraja[Fayil] < Girma) Rubuta_Tarin_bayani(Fayil, Tsawo_Daraja[Fayil]++, 0);
        Tsawo_Daraja[Fayil] = Girma; return 0;
    }
    public static int share_Mashigar_bayanai() {
        if (Hanyar_shiga_Tsawo == 0) return -22;
        int 결과 = Gajarta_kimar_bayanai_Daraja(); if (결과 < 0) return 결과;
        if (nema_ma_ajiya(정규길이) >= 0) return -21;
        결과 = 부모확인(); if (결과 < 0) return 결과;
        int Fayil = nema_Mashigar_bayanai();
        if (Fayil < 0) return -2;
        이름길이[Fayil] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void Mashigar_bayanai_Jeri() {
        Hanyar_shiga_Fara(1); Hanyar_shiga_bayit(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int Indes) {
        if (Indes < 0 || Indes >= 파일수 || 이름길이[Indes] == 0) return 0;
        for (int Warware_Indes = 0; Warware_Indes < 이름길이[Indes]; Warware_Indes++) if (Suna[Indes * 64 + Warware_Indes] == '/') return 0;
        return 이름길이[Indes];
    }
    public static int 공개이름바이트(int Indes, int 자리) {
        return Indes >= 0 && Indes < 파일수 && 자리 >= 0 && 자리 < 이름길이[Indes] ? Suna[Indes * 64 + 자리] : -22;
    }
    public static int 공개파일크기(int Indes) { return Indes >= 0 && Indes < 파일수 ? Tsawo_Daraja[Indes] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], ma_ajiya_Suna = new int[16 * 64], ma_ajiya_Tsawo = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Tafiyar_da, int Hanyar_shiga_Daraja, int[] kyamarar_gaba_Daraja, int Layin_Tazara_Hanyar_shiga) {
        if (Hanyar_shiga_Daraja < Layin_Tazara_Hanyar_shiga) return false;
        for (int Warware_Indes = 0; Warware_Indes < Layin_Tazara_Hanyar_shiga; Warware_Indes++) if (이름들[Tafiyar_da + Warware_Indes] != kyamarar_gaba_Daraja[Warware_Indes]) return false;
        return true;
    }
    static int Gajarta_kimar_bayanai_Daraja() {
        if (Hanyar_shiga_Tsawo == 0) return -22;
        정규길이 = Hanyar_shiga[0] == '/' ? 0 : 현재길이;
        for (int Warware_Indes = 0; Warware_Indes < 정규길이; Warware_Indes++) 정규[Warware_Indes] = 현재[Warware_Indes];
        int 읽는자리 = 0;
        while (읽는자리 < Hanyar_shiga_Tsawo) {
            while (읽는자리 < Hanyar_shiga_Tsawo && Hanyar_shiga[읽는자리] == '/') 읽는자리++;
            int 시작자리 = 읽는자리; while (읽는자리 < Hanyar_shiga_Tsawo && Hanyar_shiga[읽는자리] != '/') { if (Hanyar_shiga[읽는자리] == 0) return -22; 읽는자리++; }
            int 항목수 = 읽는자리 - 시작자리; if (항목수 == 0 || 항목수 == 1 && Hanyar_shiga[시작자리] == '.') continue;
            if (항목수 == 2 && Hanyar_shiga[시작자리] == '.' && Hanyar_shiga[시작자리 + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + 항목수 + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Warware_Indes = 시작자리; Warware_Indes < 읽는자리; Warware_Indes++) 정규[정규길이++] = Hanyar_shiga[Warware_Indes];
        }
        return 0;
    }
    static int nema_ma_ajiya(int 항목수) {
        if (항목수 == 0) return 0;
        for (int Warware_Indes = 1; Warware_Indes < 16; Warware_Indes++) if (ma_ajiya_Tsawo[Warware_Indes] == 항목수 && 접두(ma_ajiya_Suna, Warware_Indes * 64, 항목수, 정규, 항목수)) return Warware_Indes;
        return -1;
    }
    static int 부모확인() {
        int 항목수 = 정규길이; while (항목수 > 0 && 정규[항목수 - 1] != '/') 항목수--;
        return nema_ma_ajiya(항목수 == 0 ? 0 : 항목수 - 1) < 0 ? -2 : 0;
    }
    public static int ƙirƙíra_ma_ajiya() {
        int 처리값 = Gajarta_kimar_bayanai_Daraja(); if (처리값 < 0) return 처리값;
        if (nema_ma_ajiya(정규길이) >= 0 || nema_Mashigar_bayanai() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Warware_Indes = 1; Warware_Indes < 16; Warware_Indes++) if (ma_ajiya_Tsawo[Warware_Indes] == 0) {
            ma_ajiya_Tsawo[Warware_Indes] = 정규길이; for (int 안쪽자리 = 0; 안쪽자리 < 정규길이; 안쪽자리++) ma_ajiya_Suna[Warware_Indes * 64 + 안쪽자리] = 정규[안쪽자리]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = Gajarta_kimar_bayanai_Daraja(); if (처리값 < 0) return 처리값;
        if (nema_ma_ajiya(정규길이) >= 0) return 2;
        return nema_Mashigar_bayanai() >= 0 ? 1 : 0;
    }
    public static int Canza_ma_ajiya() {
        int 처리값 = Gajarta_kimar_bayanai_Daraja(); if (처리값 < 0) return 처리값;
        if (nema_ma_ajiya(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Warware_Indes = 0; Warware_Indes < 현재길이; Warware_Indes++) 현재[Warware_Indes] = 정규[Warware_Indes]; return 0;
    }
    public static int Cire_ma_ajiya() {
        int 처리값 = Gajarta_kimar_bayanai_Daraja(); if (처리값 < 0) return 처리값;
        int 폴더번호 = nema_ma_ajiya(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Warware_Indes = 0; Warware_Indes < 파일수; Warware_Indes++) {
            if (이름길이[Warware_Indes] > 정규길이 && 접두(Suna, Warware_Indes * 64, 이름길이[Warware_Indes], 정규, 정규길이) && Suna[Warware_Indes * 64 + 정규길이] == '/') return -39;
        }
        for (int Warware_Indes = 0; Warware_Indes < 16; Warware_Indes++) {
            if (ma_ajiya_Tsawo[Warware_Indes] > 정규길이 && 접두(ma_ajiya_Suna, Warware_Indes * 64, ma_ajiya_Tsawo[Warware_Indes], 정규, 정규길이) && ma_ajiya_Suna[Warware_Indes * 64 + 정규길이] == '/') return -39;
        }
        ma_ajiya_Tsawo[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= 파일수 || 이름길이[원본번호] == 0) return -2;
        int 처리값 = Gajarta_kimar_bayanai_Daraja(); if (처리값 < 0) return 처리값;
        if (nema_ma_ajiya(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = nema_Mashigar_bayanai(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Warware_Indes = 0; Warware_Indes < 정규길이; Warware_Indes++) Suna[원본번호 * 64 + Warware_Indes] = 정규[Warware_Indes]; return 0;
    }
    static int Mashigar_bayanai_Fara(int[] Tarin_bayani_TSARI, int 시작점, int 항목수) {
        if (!접두(Tarin_bayani_TSARI, 시작점, 항목수, 정규, 정규길이)) return -1;
        int 시작자리 = 정규길이;
        if (시작자리 > 0) { if (항목수 <= 시작자리 || Tarin_bayani_TSARI[시작점 + 시작자리] != '/') return -1; 시작자리++; }
        if (항목수 <= 시작자리) return -1;
        for (int Warware_Indes = 시작자리; Warware_Indes < 항목수; Warware_Indes++) if (Tarin_bayani_TSARI[시작점 + Warware_Indes] == '/') return -1;
        return 시작자리;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Warware_Indes = 0; Warware_Indes < 현재길이; Warware_Indes++) 보드.직렬쓰기(현재[Warware_Indes]); }
    static int 경로목록() {
        int 처리값 = Gajarta_kimar_bayanai_Daraja(); if (처리값 < 0) return 처리값;
        int Fayil_tageti = nema_Mashigar_bayanai();
        if (Fayil_tageti >= 0) { for (int Warware_Indes = 0; Warware_Indes < 정규길이; Warware_Indes++) 보드.직렬쓰기(정규[Warware_Indes]); 단말.Yi_Rubutu("  "); 단말.수(Tsawo_Daraja[Fayil_tageti]); 단말.Yi_Rubutu("bayit_Daraja(주기억 Fayil)\n"); return 0; }
        if (nema_ma_ajiya(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (ma_ajiya_Tsawo[뒷값] > 0) {
            int 시작자리 = Mashigar_bayanai_Fara(ma_ajiya_Suna, 뒷값 * 64, ma_ajiya_Tsawo[뒷값]); if (시작자리 < 0) continue;
            for (int Warware_Indes = 시작자리; Warware_Indes < ma_ajiya_Tsawo[뒷값]; Warware_Indes++) 보드.직렬쓰기(ma_ajiya_Suna[뒷값 * 64 + Warware_Indes]); 단말.Yi_Rubutu("/\n");
        }
        for (int Fayil_Indes = 0; Fayil_Indes < 파일수; Fayil_Indes++) if (이름길이[Fayil_Indes] > 0) {
            int 시작자리 = Mashigar_bayanai_Fara(Suna, Fayil_Indes * 64, 이름길이[Fayil_Indes]); if (시작자리 < 0) continue;
            for (int Warware_Indes = 시작자리; Warware_Indes < 이름길이[Fayil_Indes]; Warware_Indes++) 보드.직렬쓰기(Suna[Fayil_Indes * 64 + Warware_Indes]);
            단말.Yi_Rubutu("  "); 단말.수(Tsawo_Daraja[Fayil_Indes]); 단말.Yi_Rubutu("bayit_Daraja(주기억 Fayil)\n");
        }
        return 0;
    }
}
