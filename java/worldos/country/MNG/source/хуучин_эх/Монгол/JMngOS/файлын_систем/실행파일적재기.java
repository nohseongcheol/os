// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.JMngOS.файлын_систем;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian Гүйцэтгэх_команд 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class хэсэг_утга {
        private final int 종류;
        private final int дарцаг_утга;
        private final int хаяг;
        private final int 파일위치;
        private final int Хэмжээ;

        хэсэг_утга(int 종류, int дарцаг_утга, int хаяг, int 파일위치, int Хэмжээ) {
            this.종류 = 종류;
            this.дарцаг_утга = дарцаг_утга;
            this.хаяг = хаяг;
            this.파일위치 = 파일위치;
            this.Хэмжээ = Хэмжээ;
        }

        public int 종류() {
            return 종류;
        }

        public int дарцаг_утга() {
            return дарцаг_утга;
        }

        public int хаяг() {
            return хаяг;
        }

        public int 파일위치() {
            return 파일위치;
        }

        public int Хэмжээ() {
            return Хэмжээ;
        }
    }

    public static final class зураг {
        private final int Эхлэл_хаяг;
        private final List<хэсэг_утга> 구역들;

        зураг(int Эхлэл_хаяг, List<хэсэг_утга> 구역들) {
            this.Эхлэл_хаяг = Эхлэл_хаяг;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int Эхлэл_хаяг() {
            return Эхлэл_хаяг;
        }

        public List<хэсэг_утга> 구역들() {
            return 구역들;
        }
    }

    public зураг 검사(byte[] өгөгдөл) {
        if (өгөгдөл == null || өгөгдөл.length < 52
                || өгөгдөл[0] != 0x7f || өгөгдөл[1] != 'E' || өгөгдөл[2] != 'L' || өгөгдөл[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (өгөгдөл[4] != 1 || өгөгдөл[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int Эхлэл_хаяг = задлан_ялгал_хийх_бүхэл_тоо(өгөгдөл, 24);
        int 구역표위치 = задлан_ялгал_хийх_бүхэл_тоо(өгөгдөл, 32);
        int хэсэг_оролт_хэмжээ = 짧은정수읽기(өгөгдөл, 46);
        int 구역수 = 짧은정수읽기(өгөгдөл, 48);
        if (хэсэг_оролт_хэмжээ < 40 || 구역표위치 < 0
                || (long) 구역표위치 + (long) хэсэг_оролт_хэмжээ * 구역수 > өгөгдөл.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<хэсэг_утга> 구역들 = new ArrayList<хэсэг_утга>();
        for (int индекс = 0; индекс < 구역수; индекс++) {
            int 위치 = 구역표위치 + индекс * хэсэг_оролт_хэмжээ;
            int 종류 = задлан_ялгал_хийх_бүхэл_тоо(өгөгдөл, 위치 + 4);
            int дарцаг_утга = задлан_ялгал_хийх_бүхэл_тоо(өгөгдөл, 위치 + 8);
            int хаяг = задлан_ялгал_хийх_бүхэл_тоо(өгөгдөл, 위치 + 12);
            int 파일위치 = задлан_ялгал_хийх_бүхэл_тоо(өгөгдөл, 위치 + 16);
            int Хэмжээ = задлан_ялгал_хийх_бүхэл_тоо(өгөгдөл, 위치 + 20);
            if (Хэмжээ < 0 || (종류 != 8 && ((long) 파일위치 + Хэмжээ > өгөгдөл.length || 파일위치 < 0))) {
                throw new IllegalArgumentException("ELF хэсэг_утга өгөгдөл 범위가 올바르지 않습니다.");
            }
            구역들.add(new хэсэг_утга(종류, дарцаг_утга, хаяг, 파일위치, Хэмжээ));
        }
        return new зураг(Эхлэл_хаяг, 구역들);
    }

    private int задлан_ялгал_хийх_бүхэл_тоо(byte[] өгөгдөл, int 위치) {
        if (위치 < 0 || 위치 > өгөгдөл.length - 4) {
            throw new IllegalArgumentException("ELF бүхэл_тоо 범위를 벗어났습니다.");
        }
        return (өгөгдөл[위치] & 0xff)
                | ((өгөгдөл[위치 + 1] & 0xff) << 8)
                | ((өгөгдөл[위치 + 2] & 0xff) << 16)
                | ((өгөгдөл[위치 + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] өгөгдөл, int 위치) {
        if (위치 < 0 || 위치 > өгөгдөл.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 бүхэл_тоо 범위를 벗어났습니다.");
        }
        return (өгөгдөл[위치] & 0xff) | ((өгөгдөл[위치 + 1] & 0xff) << 8);
    }
}
