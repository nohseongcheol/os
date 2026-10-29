// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM file 64개, 파일당 16384바이트, 서술자 16개. 모든 data/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 error 번호다.
 */
public final class Memory_Mga_File {
    static final int file_COUNT = 64;
    static int[] pangalan = new int[file_COUNT * 64];
    static int[] 이름길이 = new int[file_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Nilalaman_VALUE = new int[file_COUNT * 4096];
    static int[] haba_VALUE = new int[file_COUNT];
    static int[] Sanggunian_COUNT = new int[file_COUNT];
    static int[] 사용 = new int[16];
    static int[] layunin = new int[16];
    static int[] posisyon = new int[16];
    static int[] pamamaraan_MODE = new int[16];
    static int[] path = new int[64];
    static int path_haba;

    public static int 파일한도() { return file_COUNT; }
    static int 자료읽기(int file, int posisyon_INDEX) { return (Nilalaman_VALUE[file * 4096 + posisyon_INDEX / 4] >>> ((posisyon_INDEX & 3) * 8)) & 255; }
    static void sumulat_data(int file, int posisyon_INDEX, int VALUE) {
        int espasyo_pagpasok = file * 4096 + posisyon_INDEX / 4, ilipat_VALUE = (posisyon_INDEX & 3) * 8;
        Nilalaman_VALUE[espasyo_pagpasok] = (Nilalaman_VALUE[espasyo_pagpasok] & ~(255 << ilipat_VALUE)) | ((VALUE & 255) << ilipat_VALUE);
    }

    public static int path_Start(int sukat_82232621) {
        path_haba = 0;
        if (sukat_82232621 < 1 || sukat_82232621 > 63) return -36;
        path_haba = sukat_82232621;
        for (int Loop_INDEX = 0; Loop_INDEX < sukat_82232621; Loop_INDEX++) path[Loop_INDEX] = 0;
        return 0;
    }
    public static int path_byte(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= path_haba || VALUE < 1 || VALUE > 255) return -22;
        path[INDEX] = VALUE; return 0;
    }
    static int FIND_pagpasok() {
        for (int file_INDEX = 0; file_INDEX < file_COUNT; file_INDEX++) if (이름길이[file_INDEX] > 0 && 이름길이[file_INDEX] == 정규길이 && 접두(pangalan, file_INDEX * 64, 이름길이[file_INDEX], 정규, 정규길이)) return file_INDEX;
        return -1;
    }
    public static int buksan(int 플래그) {
        if (path_haba == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < path_haba; Loop_INDEX++) if (path[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int sukat = normalisahin_VALUE(); if (sukat < 0) return sukat;
        if (FIND_Directory(정규길이) >= 0) return -21;
        sukat = 부모확인(); if (sukat < 0) return sukat;
        int file = FIND_pagpasok();
        if (file >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (file < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (사용[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (file < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < file_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Sanggunian_COUNT[Loop_INDEX] == 0) { file = Loop_INDEX; break; }
            if (file < 0) return -28;
            이름길이[file] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) pangalan[file * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            haba_VALUE[file] = 0;
        }
        if ((플래그 & 0x200) != 0) haba_VALUE[file] = 0;
        사용[서술자] = 1; layunin[서술자] = file; posisyon[서술자] = 0; pamamaraan_MODE[서술자] = 플래그;
        Sanggunian_COUNT[file]++;
        return 서술자 + 3;
    }
    static int tiyakin_kumpirmahin(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int 읽기(int 서술자) {
        int espasyo_pagpasok = tiyakin_kumpirmahin(서술자);
        if (espasyo_pagpasok < 0 || (pamamaraan_MODE[espasyo_pagpasok] & 3) == 1) return -9;
        int file = layunin[espasyo_pagpasok];
        if (posisyon[espasyo_pagpasok] >= haba_VALUE[file]) return 256; // EOF와 totoo_data 0x00..0xff 구별
        return 자료읽기(file, posisyon[espasyo_pagpasok]++);
    }
    public static int sumulat(int 서술자, int VALUE) {
        int espasyo_pagpasok = tiyakin_kumpirmahin(서술자);
        if (espasyo_pagpasok < 0 || (pamamaraan_MODE[espasyo_pagpasok] & 3) == 0) return -9;
        int file = layunin[espasyo_pagpasok];
        if ((pamamaraan_MODE[espasyo_pagpasok] & 0x400) != 0) posisyon[espasyo_pagpasok] = haba_VALUE[file];
        if (posisyon[espasyo_pagpasok] >= 16384) return -28;
        while (haba_VALUE[file] < posisyon[espasyo_pagpasok]) sumulat_data(file, haba_VALUE[file]++, 0);
        sumulat_data(file, posisyon[espasyo_pagpasok]++, VALUE);
        if (haba_VALUE[file] < posisyon[espasyo_pagpasok]) haba_VALUE[file] = posisyon[espasyo_pagpasok];
        return 1;
    }
    public static int i_seek_posisyon(int 서술자, int 거리, int Project_root) {
        int espasyo_pagpasok = tiyakin_kumpirmahin(서술자);
        if (espasyo_pagpasok < 0) return -9;
        if (Project_root < 0 || Project_root > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_root == 0 ? 0 : Project_root == 1 ? posisyon[espasyo_pagpasok] : haba_VALUE[layunin[espasyo_pagpasok]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        posisyon[espasyo_pagpasok] = 새위치; return 새위치;
    }
    public static int isara(int 서술자) {
        int espasyo_pagpasok = tiyakin_kumpirmahin(서술자);
        if (espasyo_pagpasok < 0) return -9;
        Sanggunian_COUNT[layunin[espasyo_pagpasok]]--; 사용[espasyo_pagpasok] = 0; return 0;
    }
    public static int sukat_82232621(int 서술자) {
        int espasyo_pagpasok = tiyakin_kumpirmahin(서술자); return espasyo_pagpasok < 0 ? -9 : haba_VALUE[layunin[espasyo_pagpasok]];
    }
    public static int set_haba(int 서술자, int sukat_82232621) {
        int espasyo_pagpasok = tiyakin_kumpirmahin(서술자);
        if (espasyo_pagpasok < 0 || (pamamaraan_MODE[espasyo_pagpasok] & 3) == 0) return -9;
        if (sukat_82232621 < 0 || sukat_82232621 > 16384) return -22;
        int file = layunin[espasyo_pagpasok];
        while (haba_VALUE[file] < sukat_82232621) sumulat_data(file, haba_VALUE[file]++, 0);
        haba_VALUE[file] = sukat_82232621; return 0;
    }
    public static int burahin_pagpasok() {
        if (path_haba == 0) return -22;
        int sukat = normalisahin_VALUE(); if (sukat < 0) return sukat;
        if (FIND_Directory(정규길이) >= 0) return -21;
        sukat = 부모확인(); if (sukat < 0) return sukat;
        int file = FIND_pagpasok();
        if (file < 0) return -2;
        이름길이[file] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void pagpasok_list() {
        path_Start(1); path_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= file_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (pangalan[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int posisyon_INDEX) {
        return INDEX >= 0 && INDEX < file_COUNT && posisyon_INDEX >= 0 && posisyon_INDEX < 이름길이[INDEX] ? pangalan[INDEX * 64 + posisyon_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < file_COUNT ? haba_VALUE[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], Directory_pangalan = new int[16 * 64], Directory_haba = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int run, int path_VALUE, int[] nasa_harap_VALUE, int pagitan_ng_linya_path) {
        if (path_VALUE < pagitan_ng_linya_path) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < pagitan_ng_linya_path; Loop_INDEX++) if (이름들[run + Loop_INDEX] != nasa_harap_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normalisahin_VALUE() {
        if (path_haba == 0) return -22;
        정규길이 = path[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < path_haba) {
            while (읽는자리 < path_haba && path[읽는자리] == '/') 읽는자리++;
            int Start_posisyon = 읽는자리; while (읽는자리 < path_haba && path[읽는자리] != '/') { if (path[읽는자리] == 0) return -22; 읽는자리++; }
            int pagpasok_COUNT = 읽는자리 - Start_posisyon; if (pagpasok_COUNT == 0 || pagpasok_COUNT == 1 && path[Start_posisyon] == '.') continue;
            if (pagpasok_COUNT == 2 && path[Start_posisyon] == '.' && path[Start_posisyon + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + pagpasok_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Start_posisyon; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = path[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Directory(int pagpasok_COUNT) {
        if (pagpasok_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Directory_haba[Loop_INDEX] == pagpasok_COUNT && 접두(Directory_pangalan, Loop_INDEX * 64, pagpasok_COUNT, 정규, pagpasok_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int pagpasok_COUNT = 정규길이; while (pagpasok_COUNT > 0 && 정규[pagpasok_COUNT - 1] != '/') pagpasok_COUNT--;
        return FIND_Directory(pagpasok_COUNT == 0 ? 0 : pagpasok_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int Create_Directory() {
        int 처리값 = normalisahin_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Directory(정규길이) >= 0 || FIND_pagpasok() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (Directory_haba[Loop_INDEX] == 0) {
            Directory_haba[Loop_INDEX] = 정규길이; for (int inner_join_posisyon = 0; inner_join_posisyon < 정규길이; inner_join_posisyon++) Directory_pangalan[Loop_INDEX * 64 + inner_join_posisyon] = 정규[inner_join_posisyon]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalisahin_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Directory(정규길이) >= 0) return 2;
        return FIND_pagpasok() >= 0 ? 1 : 0;
    }
    public static int baguhin_Directory() {
        int 처리값 = normalisahin_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Directory(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int tanggalin_Directory() {
        int 처리값 = normalisahin_VALUE(); if (처리값 < 0) return 처리값;
        int 폴더번호 = FIND_Directory(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < file_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(pangalan, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && pangalan[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (Directory_haba[Loop_INDEX] > 정규길이 && 접두(Directory_pangalan, Loop_INDEX * 64, Directory_haba[Loop_INDEX], 정규, 정규길이) && Directory_pangalan[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        Directory_haba[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= file_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalisahin_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Directory(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_pagpasok(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) pangalan[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int pagpasok_Start(int[] data_ARRAY, int 시작점, int pagpasok_COUNT) {
        if (!접두(data_ARRAY, 시작점, pagpasok_COUNT, 정규, 정규길이)) return -1;
        int Start_posisyon = 정규길이;
        if (Start_posisyon > 0) { if (pagpasok_COUNT <= Start_posisyon || data_ARRAY[시작점 + Start_posisyon] != '/') return -1; Start_posisyon++; }
        if (pagpasok_COUNT <= Start_posisyon) return -1;
        for (int Loop_INDEX = Start_posisyon; Loop_INDEX < pagpasok_COUNT; Loop_INDEX++) if (data_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Start_posisyon;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) board.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalisahin_VALUE(); if (처리값 < 0) return 처리값;
        int file_layunin = FIND_pagpasok();
        if (file_layunin >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) board.직렬쓰기(정규[Loop_INDEX]); 단말.sumulat("  "); 단말.수(haba_VALUE[file_layunin]); 단말.sumulat("byte_VALUE(주기억 file)\n"); return 0; }
        if (FIND_Directory(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (Directory_haba[뒷값] > 0) {
            int Start_posisyon = pagpasok_Start(Directory_pangalan, 뒷값 * 64, Directory_haba[뒷값]); if (Start_posisyon < 0) continue;
            for (int Loop_INDEX = Start_posisyon; Loop_INDEX < Directory_haba[뒷값]; Loop_INDEX++) board.직렬쓰기(Directory_pangalan[뒷값 * 64 + Loop_INDEX]); 단말.sumulat("/\n");
        }
        for (int file_INDEX = 0; file_INDEX < file_COUNT; file_INDEX++) if (이름길이[file_INDEX] > 0) {
            int Start_posisyon = pagpasok_Start(pangalan, file_INDEX * 64, 이름길이[file_INDEX]); if (Start_posisyon < 0) continue;
            for (int Loop_INDEX = Start_posisyon; Loop_INDEX < 이름길이[file_INDEX]; Loop_INDEX++) board.직렬쓰기(pangalan[file_INDEX * 64 + Loop_INDEX]);
            단말.sumulat("  "); 단말.수(haba_VALUE[file_INDEX]); 단말.sumulat("byte_VALUE(주기억 file)\n");
        }
        return 0;
    }
}
