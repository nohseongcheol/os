// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package کانادا.JCanOS.سیستم_پرونده;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 پرونده 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final سیستم_پرونده.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(سیستم_پرونده.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final سیستم_پرونده سیستم_پرونده;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(سیستم_پرونده سیستم_پرونده) {
        this.سیستم_پرونده = سیستم_پرونده;
    }

    public int باز_کردن(String نام) {
        سیستم_پرونده.열린파일 열린파일 = سیستم_پرونده.باز_کردن(نام);
        if (열린파일 == null) {
            return -2;
        }
        int فهرست = خالی_فهرست(3);
        if (فهرست < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(فهرست), new 서술자(열린파일));
        return فهرست;
    }

    public int خواندن(int فهرست, byte[] 받을곳, int اندازه) {
        서술자 ورودی_مقدار = 서술자들.get(Integer.valueOf(فهرست));
        if (ورودی_مقدار == null) {
            return -9;
        }
        if (اندازه < 0 || اندازه > 받을곳.length) {
            return -22;
        }
        int 남음 = ورودی_مقدار.열린파일.داده_ها.length - ورودی_مقدار.열린파일.مرتب_کردن;
        int 읽을크기 = Math.min(اندازه, Math.max(남음, 0));
        System.arraycopy(ورودی_مقدار.열린파일.داده_ها, ورودی_مقدار.열린파일.مرتب_کردن, 받을곳, 0, 읽을크기);
        ورودی_مقدار.열린파일.مرتب_کردن += 읽을크기;
        return 읽을크기;
    }

    public int انتقال_مرتب_کردن(int فهرست, int 거리, int نمایش_دادن_جذر) {
        서술자 ورودی_مقدار = 서술자들.get(Integer.valueOf(فهرست));
        if (ورودی_مقدار == null) {
            return -9;
        }
        int زمینه_مقدار_0764f371;
        if (نمایش_دادن_جذر == 0) {
            زمینه_مقدار_0764f371 = 0;
        } else if (نمایش_دادن_جذر == 1) {
            زمینه_مقدار_0764f371 = ورودی_مقدار.열린파일.مرتب_کردن;
        } else if (نمایش_دادن_جذر == 2) {
            زمینه_مقدار_0764f371 = ورودی_مقدار.열린파일.داده_ها.length;
        } else {
            return -22;
        }
        int 새위치 = زمینه_مقدار_0764f371 + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ورودی_مقدار.열린파일.مرتب_کردن = 새위치;
        return 새위치;
    }

    public int بستن(int فهرست) {
        서술자 ورودی_مقدار = 서술자들.remove(Integer.valueOf(فهرست));
        if (ورودی_مقدار == null) {
            return -9;
        }
        ورودی_مقدار.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int فهرست, int 최소번호) {
        서술자 ورودی_مقدار = 서술자들.get(Integer.valueOf(فهرست));
        if (ورودی_مقدار == null) {
            return -9;
        }
        int 새번호 = خالی_فهرست(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ورودی_مقدار.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ورودی_مقدار.열린파일));
        return 새번호;
    }

    public int 지정복제(int فهرست, int 새번호) {
        if (فهرست == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(فهرست)) ? فهرست : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(فهرست));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            بستن(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int فهرست, boolean مقدار) {
        서술자 ورودی_مقدار = 서술자들.get(Integer.valueOf(فهرست));
        if (ورودی_مقدار == null) {
            return -9;
        }
        ورودی_مقدار.실행시닫기 = مقدار;
        return 0;
    }

    public int 실행시닫기값(int فهرست) {
        서술자 ورودی_مقدار = 서술자들.get(Integer.valueOf(فهرست));
        if (ورودی_مقدار == null) {
            return -9;
        }
        return ورودی_مقدار.실행시닫기 ? 1 : 0;
    }

    public فایل_اطلاعات اطلاعات_سیستم(int فهرست) {
        if (فهرست >= 0 && فهرست <= 2) {
            return new فایل_اطلاعات(0, 0020666);
        }
        서술자 ورودی_مقدار = 서술자들.get(Integer.valueOf(فهرست));
        if (ورودی_مقدار == null) {
            return null;
        }
        return new فایل_اطلاعات(ورودی_مقدار.열린파일.داده_ها.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer فهرست : 번호들) {
            서술자 ورودی_مقدار = 서술자들.get(فهرست);
            if (ورودی_مقدار != null && ورودی_مقدار.실행시닫기) {
                بستن(فهرست.intValue());
            }
        }
    }

    public boolean فناوری_اطلاعات_ایجاد(int فهرست) {
        return 서술자들.containsKey(Integer.valueOf(فهرست));
    }

    public 파일서술자표 복제() {
        파일서술자표 سنجش = new 파일서술자표(سیستم_پرونده);
        for (Map.Entry<Integer, 서술자> ورودی_مقدار : 서술자들.entrySet()) {
            ورودی_مقدار.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ورودی_مقدار.getValue().열린파일);
            새서술자.실행시닫기 = ورودی_مقدار.getValue().실행시닫기;
            سنجش.서술자들.put(ورودی_مقدار.getKey(), 새서술자);
        }
        return سنجش;
    }

    private int خالی_فهرست(int 최소번호) {
        for (int فهرست = Math.max(0, 최소번호); فهرست < 최대서술자; فهرست++) {
            if (!서술자들.containsKey(Integer.valueOf(فهرست))) {
                return فهرست;
            }
        }
        return -1;
    }
}
