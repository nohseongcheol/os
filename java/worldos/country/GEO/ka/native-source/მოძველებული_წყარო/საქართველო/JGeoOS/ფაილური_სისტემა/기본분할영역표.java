// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package საქართველო.JGeoOS.ფაილური_სისტემა;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ნაგულისხმევი_მნიშვნელობა 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class დანაყოფი_მნიშვნელობა {
        private final int 종류;
        private final long დაწყება_სექცია;
        private final long 구역수;

        დანაყოფი_მნიშვნელობა(int 종류, long დაწყება_სექცია, long 구역수) {
            this.종류 = 종류;
            this.დაწყება_სექცია = დაწყება_სექცია;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long დაწყება_სექცია() { return დაწყება_სექცია; }
        public long 구역수() { return 구역수; }
    }

    public List<დანაყოფი_მნიშვნელობა> კითხვა(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<დანაყოფი_მნიშვნელობა> გაზომვა = new ArrayList<დანაყოფი_მნიშვნელობა>();
        for (int ინდექსი = 0; ინდექსი < 4; ინდექსი++) {
            int პოზიცია = 446 + ინდექსი * 16;
            int 종류 = 첫구역[პოზიცია + 4] & 0xff;
            long გაშვება = 작은순서정수(첫구역, პოზიცია + 8);
            long ზომა = 작은순서정수(첫구역, პოზიცია + 12);
            if (종류 != 0 && ზომა != 0) {
                გაზომვა.add(new დანაყოფი_მნიშვნელობა(종류, გაშვება, ზომა));
            }
        }
        return Collections.unmodifiableList(გაზომვა);
    }

    private long 작은순서정수(byte[] მონაცემები, int პოზიცია) {
        return (მონაცემები[პოზიცია] & 0xffL)
                | ((მონაცემები[პოზიცია + 1] & 0xffL) << 8)
                | ((მონაცემები[პოზიცია + 2] & 0xffL) << 16)
                | ((მონაცემები[პოზიცია + 3] & 0xffL) << 24);
    }
}

