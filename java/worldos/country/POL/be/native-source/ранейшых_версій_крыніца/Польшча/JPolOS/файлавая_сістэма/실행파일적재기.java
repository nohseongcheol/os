// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польшча.JPolOS.файлавая_сістэма;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian выканаць_каманда 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class секцыя_значэнне {
        private final int 종류;
        private final int пазнака_значэнне;
        private final int адрас;
        private final int 파일위치;
        private final int Памер;

        секцыя_значэнне(int 종류, int пазнака_значэнне, int адрас, int 파일위치, int Памер) {
            this.종류 = 종류;
            this.пазнака_значэнне = пазнака_значэнне;
            this.адрас = адрас;
            this.파일위치 = 파일위치;
            this.Памер = Памер;
        }

        public int 종류() {
            return 종류;
        }

        public int пазнака_значэнне() {
            return пазнака_значэнне;
        }

        public int адрас() {
            return адрас;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Памер() {
            return Памер;
        }
    }

    public static final class выява {
        private final int Пуск_адрас;
        private final List<секцыя_значэнне> 구역들;

        выява(int Пуск_адрас, List<секцыя_значэнне> 구역들) {
            this.Пуск_адрас = Пуск_адрас;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Пуск_адрас() {
            return Пуск_адрас;
        }

        public List<секцыя_значэнне> 구역들() {
            return 구역들;
        }
    }

    public выява 검사(byte[] дадзеныя) {
        if (дадзеныя == null || дадзеныя.length < 52
                || дадзеныя[0] != 0x7f || дадзеныя[1] != 'E' || дадзеныя[2] != 'L' || дадзеныя[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (дадзеныя[4] != 1 || дадзеныя[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Пуск_адрас = 정수읽기(дадзеныя, 24);
        int 구역표위치 = 정수읽기(дадзеныя, 32);
        int секцыя_увядзенне_памер = 짧은정수읽기(дадзеныя, 46);
        int 구역수 = 짧은정수읽기(дадзеныя, 48);
        if (секцыя_увядзенне_памер < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) секцыя_увядзенне_памер * 구역수 > дадзеныя.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<секцыя_значэнне> 구역들 = new ArrayList<секцыя_значэнне>();
        for (int індэкс = 0; індэкс < 구역수; індэкс++) {
            int Пазіцыя = 구역표위치 + індэкс * секцыя_увядзенне_памер;
            int 종류 = 정수읽기(дадзеныя, Пазіцыя + 4);
            int пазнака_значэнне = 정수읽기(дадзеныя, Пазіцыя + 8);
            int адрас = 정수읽기(дадзеныя, Пазіцыя + 12);
            int 파일위치 = 정수읽기(дадзеныя, Пазіцыя + 16);
            int Памер = 정수읽기(дадзеныя, Пазіцыя + 20);
            if (Памер < 0 || (종류 != 8 && ((long) 파일위치 + Памер > дадзеныя.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF секцыя_значэнне дадзеныя 범위가 올바르지 않습니다.");
            }
            구역들.add(new секцыя_значэнне(종류, пазнака_значэнне, адрас, 파일위치, Памер));
        }
        return new выява(Пуск_адрас, 구역들);
    }

    private int 정수읽기(byte[] дадзеныя, int Пазіцыя) {
        if (Пазіцыя < 0 || Пазіцыя > дадзеныя.length - 4) {
            throw new IllegalArgumentException("ELF цэлы_лік 범위를 벗어났습니다.");
        }
        return (дадзеныя[Пазіцыя] & 0xff)
                | ((дадзеныя[Пазіцыя + 1] & 0xff) << 8)
                | ((дадзеныя[Пазіцыя + 2] & 0xff) << 16)
                | ((дадзеныя[Пазіцыя + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] дадзеныя, int Пазіцыя) {
        if (Пазіцыя < 0 || Пазіцыя > дадзеныя.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 цэлы_лік 범위를 벗어났습니다.");
        }
        return (дадзеныя[Пазіцыя] & 0xff) | ((дадзеныя[Пазіцыя + 1] & 0xff) << 8);
    }
}
