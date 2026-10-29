// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALUE format_VALUE. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] file_talahanayan = new int[1024];
    static int 바이트해시(int VALUE, int data) { return (VALUE ^ data) * 16777619; }
    static void i_clear_data() {
        for (int INDEX = 0; INDEX < 512; INDEX++) Storage_device_koneksyon.seksiyon_data[INDEX] = 0;
    }
    static int talahanayan_integer_buong_numero(int posisyon) {
        return file_talahanayan[posisyon] | file_talahanayan[posisyon + 1] << 8 | file_talahanayan[posisyon + 2] << 16 | file_talahanayan[posisyon + 3] << 24;
    }
    static void sumulat_talahanayan_integer_buong_numero(int posisyon, int VALUE) {
        for (int INDEX = 0; INDEX < 4; INDEX++) file_talahanayan[posisyon + INDEX] = (VALUE >>> (INDEX * 8)) & 255;
    }
    static boolean tseke_talahanayan() {
        for (int file = 0; file < 8; file++) {
            int haba_VALUE = 0;
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < 64; espasyo_pagpasok++) Memory_sistema_ng_file.pangalan[espasyo_pagpasok] = file_talahanayan[file * 72 + espasyo_pagpasok];
            while (haba_VALUE < 64 && Memory_sistema_ng_file.pangalan[haba_VALUE] != 0) haba_VALUE++;
            if (haba_VALUE == 0) continue;
            if (!Memory_sistema_ng_file.tseke_pangalan(Memory_sistema_ng_file.pangalan, haba_VALUE)
                || talahanayan_integer_buong_numero(file * 72 + 64) < 0 || talahanayan_integer_buong_numero(file * 72 + 64) > 16384) return false;
            for (int nasa_harap_VALUE = 0; nasa_harap_VALUE < file; nasa_harap_VALUE++) {
                boolean 같음 = file_talahanayan[nasa_harap_VALUE * 72 + haba_VALUE] == 0;
                for (int espasyo_pagpasok = 0; espasyo_pagpasok < haba_VALUE; espasyo_pagpasok++) if (file_talahanayan[nasa_harap_VALUE * 72 + espasyo_pagpasok] != Memory_sistema_ng_file.pangalan[espasyo_pagpasok]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Start_seksiyon = 1 + 보존본 * 259;
        if (Storage_device_koneksyon.읽기(Start_seksiyon) < 0 || Storage_device_koneksyon.mag_parse_integer_buong_numero(0) != 0x4a4b534e) return -1;
        int 세대 = Storage_device_koneksyon.mag_parse_integer_buong_numero(4), checksum = Storage_device_koneksyon.mag_parse_integer_buong_numero(8);
        if (세대 < 1 || Storage_device_koneksyon.mag_parse_integer_buong_numero(12) != (세대 ^ checksum ^ 0x4a4b534e)) return -1;
        int hash_file = 0x811c9dc5;
        for (int seksiyon_VALUE = 0; seksiyon_VALUE < 258; seksiyon_VALUE++) {
            if (Storage_device_koneksyon.읽기(Start_seksiyon + 1 + seksiyon_VALUE) < 0) return -1;
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < 512; espasyo_pagpasok++) {
                int VALUE = Storage_device_koneksyon.seksiyon_data[espasyo_pagpasok];
                hash_file = 바이트해시(hash_file, VALUE);
                if (seksiyon_VALUE < 2) file_talahanayan[seksiyon_VALUE * 512 + espasyo_pagpasok] = VALUE;
            }
        }
        return hash_file == checksum && tseke_talahanayan() ? 세대 : -1;
    }
    static int load(int 보존본) {
        int Start_seksiyon = 1 + 보존본 * 259;
        for (int seksiyon_VALUE = 0; seksiyon_VALUE < 2; seksiyon_VALUE++) {
            if (Storage_device_koneksyon.읽기(Start_seksiyon + 1 + seksiyon_VALUE) < 0) return -5;
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < 512; espasyo_pagpasok++) file_talahanayan[seksiyon_VALUE * 512 + espasyo_pagpasok] = Storage_device_koneksyon.seksiyon_data[espasyo_pagpasok];
        }
        for (int file = 0; file < 8; file++) {
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < 64; espasyo_pagpasok++) Memory_sistema_ng_file.이름들[file * 64 + espasyo_pagpasok] = file_talahanayan[file * 72 + espasyo_pagpasok];
            Memory_sistema_ng_file.sukat_list[file] = file_talahanayan[file * 72] == 0 ? 0 : talahanayan_integer_buong_numero(file * 72 + 64);
            Memory_sistema_ng_file.허가들[file] = talahanayan_integer_buong_numero(file * 72 + 68) & 511;
            for (int seksiyon_VALUE = 0; seksiyon_VALUE < 32; seksiyon_VALUE++) {
                if (Storage_device_koneksyon.읽기(Start_seksiyon + 3 + file * 32 + seksiyon_VALUE) < 0) return -5;
                int email = device_VALUE.file_Memory() + file * 16384 + seksiyon_VALUE * 512;
                for (int espasyo_pagpasok = 0; espasyo_pagpasok < 512; espasyo_pagpasok++) device_VALUE.sumulat_Memory(email + espasyo_pagpasok, Storage_device_koneksyon.seksiyon_data[espasyo_pagpasok]);
            }
        }
        return 0;
    }
    static void Ihanda() {
        if (Storage_device_koneksyon.읽기(0) < 0 || Storage_device_koneksyon.mag_parse_integer_buong_numero(0) != 0x54534b4a
            || Storage_device_koneksyon.mag_parse_integer_buong_numero(4) != 0x3145524f || Storage_device_koneksyon.mag_parse_integer_buong_numero(8) != 2048
            || Storage_device_koneksyon.mag_parse_integer_buong_numero(12) != 0x3153464a) {
            SMS_Terminal.sumulat("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Storage_device_koneksyon.information_technology_Aktibo_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.sumulat("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (load(현재보존본) < 0) {
            SMS_Terminal.sumulat("STORE read failed; halted to preserve files\n"); device_VALUE.정지();
        }
        SMS_Terminal.sumulat("STORE restored generation "); SMS_Terminal.수쓰기(세대번호); SMS_Terminal.문자(10);
    }
    static int iakma() {
        if (!Storage_device_koneksyon.information_technology_Aktibo_9e72441a) return -19;
        if (세대번호 == 2147483647) return -75;
        int Susunod_item = 현재보존본 == 0 ? 1 : 0, Start_seksiyon = 1 + Susunod_item * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 device_VALUE 캐시를 비운다.
        i_clear_data();
        if (Storage_device_koneksyon.sumulat(Start_seksiyon) < 0 || Storage_device_koneksyon.밀어쓰기() < 0) return -5;
        for (int espasyo_pagpasok = 0; espasyo_pagpasok < 1024; espasyo_pagpasok++) file_talahanayan[espasyo_pagpasok] = 0;
        for (int file = 0; file < 8; file++) if (Memory_sistema_ng_file.이름들[file * 64] != 0) {
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < 64; espasyo_pagpasok++) file_talahanayan[file * 72 + espasyo_pagpasok] = Memory_sistema_ng_file.이름들[file * 64 + espasyo_pagpasok];
            sumulat_talahanayan_integer_buong_numero(file * 72 + 64, Memory_sistema_ng_file.sukat_list[file]);
            sumulat_talahanayan_integer_buong_numero(file * 72 + 68, Memory_sistema_ng_file.허가들[file]);
        }
        int hash_file = 0x811c9dc5;
        for (int seksiyon_VALUE = 0; seksiyon_VALUE < 258; seksiyon_VALUE++) {
            for (int espasyo_pagpasok = 0; espasyo_pagpasok < 512; espasyo_pagpasok++) {
                int VALUE = 0;
                if (seksiyon_VALUE < 2) VALUE = file_talahanayan[seksiyon_VALUE * 512 + espasyo_pagpasok];
                else {
                    int file = (seksiyon_VALUE - 2) / 32, posisyon = (seksiyon_VALUE - 2) % 32 * 512 + espasyo_pagpasok;
                    if (file_talahanayan[file * 72] != 0 && posisyon < Memory_sistema_ng_file.sukat_list[file])
                        VALUE = device_VALUE.기억읽기(device_VALUE.file_Memory() + file * 16384 + posisyon);
                }
                Storage_device_koneksyon.seksiyon_data[espasyo_pagpasok] = VALUE; hash_file = 바이트해시(hash_file, VALUE);
            }
            if (Storage_device_koneksyon.sumulat(Start_seksiyon + 1 + seksiyon_VALUE) < 0) return -5;
        }
        if (Storage_device_koneksyon.밀어쓰기() < 0) return -5;
        i_clear_data(); Storage_device_koneksyon.sumulat_integer_buong_numero_VALUE(0, 0x4a4b534e);
        Storage_device_koneksyon.sumulat_integer_buong_numero_VALUE(4, 세대번호 + 1); Storage_device_koneksyon.sumulat_integer_buong_numero_VALUE(8, hash_file);
        Storage_device_koneksyon.sumulat_integer_buong_numero_VALUE(12, (세대번호 + 1) ^ hash_file ^ 0x4a4b534e);
        if (Storage_device_koneksyon.sumulat(Start_seksiyon) < 0 || Storage_device_koneksyon.밀어쓰기() < 0) return -5;
        현재보존본 = Susunod_item; 세대번호++;
        return 0;
    }
}
