// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئێران.JIrnOS.سیستمی_فایل;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 فایل 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final سیستمی_فایل.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(سیستمی_فایل.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final سیستمی_فایل سیستمی_فایل;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(سیستمی_فایل سیستمی_فایل) {
        this.سیستمی_فایل = سیستمی_فایل;
    }

    public int کردنەوە(String ناو) {
        سیستمی_فایل.열린파일 열린파일 = سیستمی_فایل.کردنەوە(ناو);
        if (열린파일 == null) {
            return -2;
        }
        int پێرست = بەتاڵ_پێرست(3);
        if (پێرست < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(پێرست), new 서술자(열린파일));
        return پێرست;
    }

    public int 읽기(int پێرست, byte[] 받을곳, int گۆڕینی_ئەندازە) {
        서술자 تێنووسین_نرخ = 서술자들.get(Integer.valueOf(پێرست));
        if (تێنووسین_نرخ == null) {
            return -9;
        }
        if (گۆڕینی_ئەندازە < 0 || گۆڕینی_ئەندازە > 받을곳.length) {
            return -22;
        }
        int 남음 = تێنووسین_نرخ.열린파일.دەیتا.length - تێنووسین_نرخ.열린파일.위치;
        int 읽을크기 = Math.min(گۆڕینی_ئەندازە, Math.max(남음, 0));
        System.arraycopy(تێنووسین_نرخ.열린파일.دەیتا, تێنووسین_نرخ.열린파일.위치, 받을곳, 0, 읽을크기);
        تێنووسین_نرخ.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int پێرست, int 거리, int 기준) {
        서술자 تێنووسین_نرخ = 서술자들.get(Integer.valueOf(پێرست));
        if (تێنووسین_نرخ == null) {
            return -9;
        }
        int بن_زمینه_نرخ;
        if (기준 == 0) {
            بن_زمینه_نرخ = 0;
        } else if (기준 == 1) {
            بن_زمینه_نرخ = تێنووسین_نرخ.열린파일.위치;
        } else if (기준 == 2) {
            بن_زمینه_نرخ = تێنووسین_نرخ.열린파일.دەیتا.length;
        } else {
            return -22;
        }
        int 새위치 = بن_زمینه_نرخ + 거리;
        if (새위치 < 0) {
            return -22;
        }
        تێنووسین_نرخ.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int داخستن(int پێرست) {
        서술자 تێنووسین_نرخ = 서술자들.remove(Integer.valueOf(پێرست));
        if (تێنووسین_نرخ == null) {
            return -9;
        }
        تێنووسین_نرخ.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int پێرست, int 최소번호) {
        서술자 تێنووسین_نرخ = 서술자들.get(Integer.valueOf(پێرست));
        if (تێنووسین_نرخ == null) {
            return -9;
        }
        int 새번호 = بەتاڵ_پێرست(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        تێنووسین_نرخ.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(تێنووسین_نرخ.열린파일));
        return 새번호;
    }

    public int 지정복제(int پێرست, int 새번호) {
        if (پێرست == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(پێرست)) ? پێرست : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(پێرست));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            داخستن(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int پێرست, boolean نرخ) {
        서술자 تێنووسین_نرخ = 서술자들.get(Integer.valueOf(پێرست));
        if (تێنووسین_نرخ == null) {
            return -9;
        }
        تێنووسین_نرخ.실행시닫기 = نرخ;
        return 0;
    }

    public int 실행시닫기값(int پێرست) {
        서술자 تێنووسین_نرخ = 서술자들.get(Integer.valueOf(پێرست));
        if (تێنووسین_نرخ == null) {
            return -9;
        }
        return تێنووسین_نرخ.실행시닫기 ? 1 : 0;
    }

    public فایل_زانیاری msinfo32_exe(int پێرست) {
        if (پێرست >= 0 && پێرست <= 2) {
            return new فایل_زانیاری(0, 0020666);
        }
        서술자 تێنووسین_نرخ = 서술자들.get(Integer.valueOf(پێرست));
        if (تێنووسین_نرخ == null) {
            return null;
        }
        return new فایل_زانیاری(تێنووسین_نرخ.열린파일.دەیتا.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer پێرست : 번호들) {
            서술자 تێنووسین_نرخ = 서술자들.get(پێرست);
            if (تێنووسین_نرخ != null && تێنووسین_نرخ.실행시닫기) {
                داخستن(پێرست.intValue());
            }
        }
    }

    public boolean 열려있음(int پێرست) {
        return 서술자들.containsKey(Integer.valueOf(پێرست));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(سیستمی_فایل);
        for (Map.Entry<Integer, 서술자> تێنووسین_نرخ : 서술자들.entrySet()) {
            تێنووسین_نرخ.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(تێنووسین_نرخ.getValue().열린파일);
            새서술자.실행시닫기 = تێنووسین_نرخ.getValue().실행시닫기;
            결과.서술자들.put(تێنووسین_نرخ.getKey(), 새서술자);
        }
        return 결과;
    }

    private int بەتاڵ_پێرست(int 최소번호) {
        for (int پێرست = Math.max(0, 최소번호); پێرست < 최대서술자; پێرست++) {
            if (!서술자들.containsKey(Integer.valueOf(پێرست))) {
                return پێرست;
            }
        }
        return -1;
    }
}
