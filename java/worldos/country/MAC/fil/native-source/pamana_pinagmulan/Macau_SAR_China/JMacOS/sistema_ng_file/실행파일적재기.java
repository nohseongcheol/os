// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Macau_SAR_China.JMacOS.sistema_ng_file;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Mag_execute_utos 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class seksiyon_VALUE {
        private final int 종류;
        private final int i_flag_VALUE;
        private final int email;
        private final int file_posisyon;
        private final int sukat_82232621;

        seksiyon_VALUE(int 종류, int i_flag_VALUE, int email, int file_posisyon, int sukat_82232621) {
            this.종류 = 종류;
            this.i_flag_VALUE = i_flag_VALUE;
            this.email = email;
            this.file_posisyon = file_posisyon;
            this.sukat_82232621 = sukat_82232621;
        }

        public int 종류() {
            return 종류;
        }

        public int i_flag_VALUE() {
            return i_flag_VALUE;
        }

        public int email() {
            return email;
        }

        public int file_posisyon() {
            return file_posisyon;
        }

        public int sukat_82232621() {
            return sukat_82232621;
        }
    }

    public static final class IMAGE {
        private final int Start_email;
        private final List<seksiyon_VALUE> 구역들;

        IMAGE(int Start_email, List<seksiyon_VALUE> 구역들) {
            this.Start_email = Start_email;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Start_email() {
            return Start_email;
        }

        public List<seksiyon_VALUE> 구역들() {
            return 구역들;
        }
    }

    public IMAGE 검사(byte[] data) {
        if (data == null || data.length < 52
                || data[0] != 0x7f || data[1] != 'E' || data[2] != 'L' || data[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (data[4] != 1 || data[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Start_email = mag_parse_integer_buong_numero(data, 24);
        int seksiyon_talahanayan_posisyon = mag_parse_integer_buong_numero(data, 32);
        int seksiyon_pagpasok_sukat = 짧은정수읽기(data, 46);
        int seksiyon_COUNT = 짧은정수읽기(data, 48);
        if (seksiyon_pagpasok_sukat < 40 || seksiyon_talahanayan_posisyon < 0
                || (long) seksiyon_talahanayan_posisyon + (long) seksiyon_pagpasok_sukat * seksiyon_COUNT > data.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<seksiyon_VALUE> 구역들 = new ArrayList<seksiyon_VALUE>();
        for (int INDEX = 0; INDEX < seksiyon_COUNT; INDEX++) {
            int posisyon = seksiyon_talahanayan_posisyon + INDEX * seksiyon_pagpasok_sukat;
            int 종류 = mag_parse_integer_buong_numero(data, posisyon + 4);
            int i_flag_VALUE = mag_parse_integer_buong_numero(data, posisyon + 8);
            int email = mag_parse_integer_buong_numero(data, posisyon + 12);
            int file_posisyon = mag_parse_integer_buong_numero(data, posisyon + 16);
            int sukat_82232621 = mag_parse_integer_buong_numero(data, posisyon + 20);
            if (sukat_82232621 < 0 || (종류 != 8 && ((long) file_posisyon + sukat_82232621 > data.length || file_posisyon < 0))) {
                throw new IllegalArgumentException("ELF seksiyon_VALUE data 범위가 올바르지 않습니다.");
            }
            구역들.add(new seksiyon_VALUE(종류, i_flag_VALUE, email, file_posisyon, sukat_82232621));
        }
        return new IMAGE(Start_email, 구역들);
    }

    private int mag_parse_integer_buong_numero(byte[] data, int posisyon) {
        if (posisyon < 0 || posisyon > data.length - 4) {
            throw new IllegalArgumentException("ELF integer_buong_numero 범위를 벗어났습니다.");
        }
        return (data[posisyon] & 0xff)
                | ((data[posisyon + 1] & 0xff) << 8)
                | ((data[posisyon + 2] & 0xff) << 16)
                | ((data[posisyon + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] data, int posisyon) {
        if (posisyon < 0 || posisyon > data.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 integer_buong_numero 범위를 벗어났습니다.");
        }
        return (data[posisyon] & 0xff) | ((data[posisyon + 1] & 0xff) << 8);
    }
}
