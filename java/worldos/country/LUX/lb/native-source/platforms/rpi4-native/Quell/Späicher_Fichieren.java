// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fichier 64개, 파일당 16384바이트, 서술자 16개. 모든 Daten/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 Feeler 번호다.
 */
public final class Späicher_Fichieren {
    static final int Fichier_COUNT = 64;
    static int[] Numm = new int[Fichier_COUNT * 64];
    static int[] 이름길이 = new int[Fichier_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Inhalt_VALUE = new int[Fichier_COUNT * 4096];
    static int[] Längt_VALUE = new int[Fichier_COUNT];
    static int[] Referenzen_COUNT = new int[Fichier_COUNT];
    static int[] 사용 = new int[16];
    static int[] Zil = new int[16];
    static int[] positionéieren = new int[16];
    static int[] Method_MODE = new int[16];
    static int[] Wee = new int[64];
    static int Wee_Längt;

    public static int 파일한도() { return Fichier_COUNT; }
    static int 자료읽기(int Fichier, int positionéieren_INDEX) { return (Inhalt_VALUE[Fichier * 4096 + positionéieren_INDEX / 4] >>> ((positionéieren_INDEX & 3) * 8)) & 255; }
    static void schreiwen_Daten(int Fichier, int positionéieren_INDEX, int VALUE) {
        int Slot_Agab = Fichier * 4096 + positionéieren_INDEX / 4, verréckelen_VALUE = (positionéieren_INDEX & 3) * 8;
        Inhalt_VALUE[Slot_Agab] = (Inhalt_VALUE[Slot_Agab] & ~(255 << verréckelen_VALUE)) | ((VALUE & 255) << verréckelen_VALUE);
    }

    public static int Wee_Start(int d_Gréisst_veränneren) {
        Wee_Längt = 0;
        if (d_Gréisst_veränneren < 1 || d_Gréisst_veränneren > 63) return -36;
        Wee_Längt = d_Gréisst_veränneren;
        for (int Loop_INDEX = 0; Loop_INDEX < d_Gréisst_veränneren; Loop_INDEX++) Wee[Loop_INDEX] = 0;
        return 0;
    }
    public static int Wee_Byte(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= Wee_Längt || VALUE < 1 || VALUE > 255) return -22;
        Wee[INDEX] = VALUE; return 0;
    }
    static int FIND_Agab() {
        for (int Fichier_INDEX = 0; Fichier_INDEX < Fichier_COUNT; Fichier_INDEX++) if (이름길이[Fichier_INDEX] > 0 && 이름길이[Fichier_INDEX] == 정규길이 && 접두(Numm, Fichier_INDEX * 64, 이름길이[Fichier_INDEX], 정규, 정규길이)) return Fichier_INDEX;
        return -1;
    }
    public static int ariichten(int 플래그) {
        if (Wee_Längt == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < Wee_Längt; Loop_INDEX++) if (Wee[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int Mooss = normaliséieren_VALUE(); if (Mooss < 0) return Mooss;
        if (FIND_Verzeechnes(정규길이) >= 0) return -21;
        Mooss = 부모확인(); if (Mooss < 0) return Mooss;
        int Fichier = FIND_Agab();
        if (Fichier >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fichier < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Fichier < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Fichier_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Referenzen_COUNT[Loop_INDEX] == 0) { Fichier = Loop_INDEX; break; }
            if (Fichier < 0) return -28;
            이름길이[Fichier] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Numm[Fichier * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            Längt_VALUE[Fichier] = 0;
        }
        if ((플래그 & 0x200) != 0) Längt_VALUE[Fichier] = 0;
        사용[서술자] = 1; Zil[서술자] = Fichier; positionéieren[서술자] = 0; Method_MODE[서술자] = 플래그;
        Referenzen_COUNT[Fichier]++;
        return 서술자 + 3;
    }
    static int verifizéieren(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int Slot_Agab = verifizéieren(서술자);
        if (Slot_Agab < 0 || (Method_MODE[Slot_Agab] & 3) == 1) return -9;
        int Fichier = Zil[Slot_Agab];
        if (positionéieren[Slot_Agab] >= Längt_VALUE[Fichier]) return 256; // EOF와 aktuell_Daten 0x00..0xff 구별
        return 자료읽기(Fichier, positionéieren[Slot_Agab]++);
    }
    public static int schreiwen(int 서술자, int VALUE) {
        int Slot_Agab = verifizéieren(서술자);
        if (Slot_Agab < 0 || (Method_MODE[Slot_Agab] & 3) == 0) return -9;
        int Fichier = Zil[Slot_Agab];
        if ((Method_MODE[Slot_Agab] & 0x400) != 0) positionéieren[Slot_Agab] = Längt_VALUE[Fichier];
        if (positionéieren[Slot_Agab] >= 16384) return -28;
        while (Längt_VALUE[Fichier] < positionéieren[Slot_Agab]) schreiwen_Daten(Fichier, Längt_VALUE[Fichier]++, 0);
        schreiwen_Daten(Fichier, positionéieren[Slot_Agab]++, VALUE);
        if (Längt_VALUE[Fichier] < positionéieren[Slot_Agab]) Längt_VALUE[Fichier] = positionéieren[Slot_Agab];
        return 1;
    }
    public static int sichen_positionéieren(int 서술자, int 거리, int projezéieren_Racinn) {
        int Slot_Agab = verifizéieren(서술자);
        if (Slot_Agab < 0) return -9;
        if (projezéieren_Racinn < 0 || projezéieren_Racinn > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (projezéieren_Racinn == 0 ? 0 : projezéieren_Racinn == 1 ? positionéieren[Slot_Agab] : Längt_VALUE[Zil[Slot_Agab]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        positionéieren[Slot_Agab] = 새위치; return 새위치;
    }
    public static int Clôture(int 서술자) {
        int Slot_Agab = verifizéieren(서술자);
        if (Slot_Agab < 0) return -9;
        Referenzen_COUNT[Zil[Slot_Agab]]--; 사용[Slot_Agab] = 0; return 0;
    }
    public static int d_Gréisst_veränneren(int 서술자) {
        int Slot_Agab = verifizéieren(서술자); return Slot_Agab < 0 ? -9 : Längt_VALUE[Zil[Slot_Agab]];
    }
    public static int Saz_Längt(int 서술자, int d_Gréisst_veränneren) {
        int Slot_Agab = verifizéieren(서술자);
        if (Slot_Agab < 0 || (Method_MODE[Slot_Agab] & 3) == 0) return -9;
        if (d_Gréisst_veränneren < 0 || d_Gréisst_veränneren > 16384) return -22;
        int Fichier = Zil[Slot_Agab];
        while (Längt_VALUE[Fichier] < d_Gréisst_veränneren) schreiwen_Daten(Fichier, Längt_VALUE[Fichier]++, 0);
        Längt_VALUE[Fichier] = d_Gréisst_veränneren; return 0;
    }
    public static int 지우기() {
        if (Wee_Längt == 0) return -22;
        int Mooss = normaliséieren_VALUE(); if (Mooss < 0) return Mooss;
        if (FIND_Verzeechnes(정규길이) >= 0) return -21;
        Mooss = 부모확인(); if (Mooss < 0) return Mooss;
        int Fichier = FIND_Agab();
        if (Fichier < 0) return -2;
        이름길이[Fichier] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void Agab_Lëscht() {
        Wee_Start(1); Wee_Byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Fichier_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Numm[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int positionéieren_INDEX) {
        return INDEX >= 0 && INDEX < Fichier_COUNT && positionéieren_INDEX >= 0 && positionéieren_INDEX < 이름길이[INDEX] ? Numm[INDEX * 64 + positionéieren_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Fichier_COUNT ? Längt_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], Verzeechnes_Numm = new int[16 * 64], Verzeechnes_Längt = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Laf, int Wee_VALUE, int[] 앞, int Anzuch_Wee) {
        if (Wee_VALUE < Anzuch_Wee) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < Anzuch_Wee; Loop_INDEX++) if (이름들[Laf + Loop_INDEX] != 앞[Loop_INDEX]) return false;
        return true;
    }
    static int normaliséieren_VALUE() {
        if (Wee_Längt == 0) return -22;
        정규길이 = Wee[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < Wee_Längt) {
            while (읽는자리 < Wee_Längt && Wee[읽는자리] == '/') 읽는자리++;
            int Start_positionéieren = 읽는자리; while (읽는자리 < Wee_Längt && Wee[읽는자리] != '/') { if (Wee[읽는자리] == 0) return -22; 읽는자리++; }
            int Agab_COUNT = 읽는자리 - Start_positionéieren; if (Agab_COUNT == 0 || Agab_COUNT == 1 && Wee[Start_positionéieren] == '.') continue;
            if (Agab_COUNT == 2 && Wee[Start_positionéieren] == '.' && Wee[Start_positionéieren + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + Agab_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Start_positionéieren; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = Wee[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Verzeechnes(int Agab_COUNT) {
        if (Agab_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Verzeechnes_Längt[Loop_INDEX] == Agab_COUNT && 접두(Verzeechnes_Numm, Loop_INDEX * 64, Agab_COUNT, 정규, Agab_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int Agab_COUNT = 정규길이; while (Agab_COUNT > 0 && 정규[Agab_COUNT - 1] != '/') Agab_COUNT--;
        return FIND_Verzeechnes(Agab_COUNT == 0 ? 0 : Agab_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Create_Verzeechnes() {
        int 처리값 = normaliséieren_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Verzeechnes(정규길이) >= 0 || FIND_Agab() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Verzeechnes_Längt[Loop_INDEX] == 0) {
            Verzeechnes_Längt[Loop_INDEX] = 정규길이; for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 정규길이; intern_Verknëppung_positionéieren++) Verzeechnes_Numm[Loop_INDEX * 64 + intern_Verknëppung_positionéieren] = 정규[intern_Verknëppung_positionéieren]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normaliséieren_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Verzeechnes(정규길이) >= 0) return 2;
        return FIND_Agab() >= 0 ? 1 : 0;
    }
    public static int änneren_Verzeechnes() {
        int 처리값 = normaliséieren_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Verzeechnes(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int ewechhuelen_Verzeechnes() {
        int 처리값 = normaliséieren_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_Verzeechnes(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Fichier_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Numm, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Numm[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (Verzeechnes_Längt[Loop_INDEX] > 정규길이 && 접두(Verzeechnes_Numm, Loop_INDEX * 64, Verzeechnes_Längt[Loop_INDEX], 정규, 정규길이) && Verzeechnes_Numm[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        Verzeechnes_Längt[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Fichier_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normaliséieren_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Verzeechnes(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_Agab(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Numm[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int Agab_Start(int[] Daten_ARRAY, int 시작점, int Agab_COUNT) {
        if (!접두(Daten_ARRAY, 시작점, Agab_COUNT, 정규, 정규길이)) return -1;
        int Start_positionéieren = 정규길이;
        if (Start_positionéieren > 0) { if (Agab_COUNT <= Start_positionéieren || Daten_ARRAY[시작점 + Start_positionéieren] != '/') return -1; Start_positionéieren++; }
        if (Agab_COUNT <= Start_positionéieren) return -1;
        for (int Loop_INDEX = Start_positionéieren; Loop_INDEX < Agab_COUNT; Loop_INDEX++) if (Daten_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Start_positionéieren;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) Board.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normaliséieren_VALUE(); if (처리값 < 0) return 처리값;
        int Fichier_Zil = FIND_Agab();
        if (Fichier_Zil >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Board.직렬쓰기(정규[Loop_INDEX]); 단말.schreiwen("  "); 단말.수(Längt_VALUE[Fichier_Zil]); 단말.schreiwen("Byte_VALUE(주기억 Fichier)\n"); return 0; }
        if (FIND_Verzeechnes(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Verzeechnes_Längt[뒷값] > 0) {
            int Start_positionéieren = Agab_Start(Verzeechnes_Numm, 뒷값 * 64, Verzeechnes_Längt[뒷값]); if (Start_positionéieren < 0) continue;
            for (int Loop_INDEX = Start_positionéieren; Loop_INDEX < Verzeechnes_Längt[뒷값]; Loop_INDEX++) Board.직렬쓰기(Verzeechnes_Numm[뒷값 * 64 + Loop_INDEX]); 단말.schreiwen("/\n");
        }
        for (int Fichier_INDEX = 0; Fichier_INDEX < Fichier_COUNT; Fichier_INDEX++) if (이름길이[Fichier_INDEX] > 0) {
            int Start_positionéieren = Agab_Start(Numm, Fichier_INDEX * 64, 이름길이[Fichier_INDEX]); if (Start_positionéieren < 0) continue;
            for (int Loop_INDEX = Start_positionéieren; Loop_INDEX < 이름길이[Fichier_INDEX]; Loop_INDEX++) Board.직렬쓰기(Numm[Fichier_INDEX * 64 + Loop_INDEX]);
            단말.schreiwen("  "); 단말.수(Längt_VALUE[Fichier_INDEX]); 단말.schreiwen("Byte_VALUE(주기억 Fichier)\n");
        }
        return 0;
    }
}
