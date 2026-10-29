// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ഖത്തർ.JQatOS.ഫയല്_സിസ്റ്റം;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 സ്ഥിരസ്ഥിതി_മൂല്യം 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class വിഭജനം_മൂല്യം {
        private final int 종류;
        private final long ആരംഭം_വിഭാഗം;
        private final long 구역수;

        വിഭജനം_മൂല്യം(int 종류, long ആരംഭം_വിഭാഗം, long 구역수) {
            this.종류 = 종류;
            this.ആരംഭം_വിഭാഗം = ആരംഭം_വിഭാഗം;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long ആരംഭം_വിഭാഗം() { return ആരംഭം_വിഭാഗം; }
        public long 구역수() { return 구역수; }
    }

    public List<വിഭജനം_മൂല്യം> വായന(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<വിഭജനം_മൂല്യം> അളവ് = new ArrayList<വിഭജനം_മൂല്യം>();
        for (int സൂചിക = 0; സൂചിക < 4; സൂചിക++) {
            int സ്ഥാനം = 446 + സൂചിക * 16;
            int 종류 = 첫구역[സ്ഥാനം + 4] & 0xff;
            long നടപ്പിലാക്കുക = 작은순서정수(첫구역, സ്ഥാനം + 8);
            long വലിപ്പം = 작은순서정수(첫구역, സ്ഥാനം + 12);
            if (종류 != 0 && വലിപ്പം != 0) {
                അളവ്.add(new വിഭജനം_മൂല്യം(종류, നടപ്പിലാക്കുക, വലിപ്പം));
            }
        }
        return Collections.unmodifiableList(അളവ്);
    }

    private long 작은순서정수(byte[] ഡാറ്റാ, int സ്ഥാനം) {
        return (ഡാറ്റാ[സ്ഥാനം] & 0xffL)
                | ((ഡാറ്റാ[സ്ഥാനം + 1] & 0xffL) << 8)
                | ((ഡാറ്റാ[സ്ഥാനം + 2] & 0xffL) << 16)
                | ((ഡാറ്റാ[സ്ഥാനം + 3] & 0xffL) << 24);
    }
}

