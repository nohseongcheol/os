// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malaysia.JMysOS.sistem_fail;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fail 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final sistem_fail.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(sistem_fail.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sistem_fail sistem_fail;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(sistem_fail sistem_fail) {
        this.sistem_fail = sistem_fail;
    }

    public int Buka(String Nama) {
        sistem_fail.열린파일 열린파일 = sistem_fail.Buka(Nama);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = 빈번호(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Baca(int INDEX, byte[] 받을곳, int Saiz) {
        서술자 pemasukan_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pemasukan_VALUE == null) {
            return -9;
        }
        if (Saiz < 0 || Saiz > 받을곳.length) {
            return -22;
        }
        int 남음 = pemasukan_VALUE.열린파일.data.length - pemasukan_VALUE.열린파일.Kedudukan;
        int 읽을크기 = Math.min(Saiz, Math.max(남음, 0));
        System.arraycopy(pemasukan_VALUE.열린파일.data, pemasukan_VALUE.열린파일.Kedudukan, 받을곳, 0, 읽을크기);
        pemasukan_VALUE.열린파일.Kedudukan += 읽을크기;
        return 읽을크기;
    }

    public int alih_jawatan(int INDEX, int 거리, int projek_akar) {
        서술자 pemasukan_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pemasukan_VALUE == null) {
            return -9;
        }
        int latar_VALUE;
        if (projek_akar == 0) {
            latar_VALUE = 0;
        } else if (projek_akar == 1) {
            latar_VALUE = pemasukan_VALUE.열린파일.Kedudukan;
        } else if (projek_akar == 2) {
            latar_VALUE = pemasukan_VALUE.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = latar_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        pemasukan_VALUE.열린파일.Kedudukan = 새위치;
        return 새위치;
    }

    public int Tutup(int INDEX) {
        서술자 pemasukan_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (pemasukan_VALUE == null) {
            return -9;
        }
        pemasukan_VALUE.열린파일.Rujukan_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 pemasukan_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pemasukan_VALUE == null) {
            return -9;
        }
        int 새번호 = 빈번호(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        pemasukan_VALUE.열린파일.Rujukan_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(pemasukan_VALUE.열린파일));
        return 새번호;
    }

    public int 지정복제(int INDEX, int 새번호) {
        if (INDEX == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Tutup(새번호);
        }
        원본.열린파일.Rujukan_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 pemasukan_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pemasukan_VALUE == null) {
            return -9;
        }
        pemasukan_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 pemasukan_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pemasukan_VALUE == null) {
            return -9;
        }
        return pemasukan_VALUE.실행시닫기 ? 1 : 0;
    }

    public fail_info msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new fail_info(0, 0020666);
        }
        서술자 pemasukan_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pemasukan_VALUE == null) {
            return null;
        }
        return new fail_info(pemasukan_VALUE.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 pemasukan_VALUE = 서술자들.get(INDEX);
            if (pemasukan_VALUE != null && pemasukan_VALUE.실행시닫기) {
                Tutup(INDEX.intValue());
            }
        }
    }

    public boolean teknologi_maklumat_buka(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 klon_VALUE() {
        파일서술자표 ukuran = new 파일서술자표(sistem_fail);
        for (Map.Entry<Integer, 서술자> pemasukan_VALUE : 서술자들.entrySet()) {
            pemasukan_VALUE.getValue().열린파일.Rujukan_COUNT++;
            서술자 새서술자 = new 서술자(pemasukan_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = pemasukan_VALUE.getValue().실행시닫기;
            ukuran.서술자들.put(pemasukan_VALUE.getKey(), 새서술자);
        }
        return ukuran;
    }

    private int 빈번호(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
