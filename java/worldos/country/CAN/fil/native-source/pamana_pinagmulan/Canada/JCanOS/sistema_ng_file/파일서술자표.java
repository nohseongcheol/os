// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.sistema_ng_file;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 file 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final sistema_ng_file.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(sistema_ng_file.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sistema_ng_file sistema_ng_file;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(sistema_ng_file sistema_ng_file) {
        this.sistema_ng_file = sistema_ng_file;
    }

    public int buksan(String pangalan) {
        sistema_ng_file.열린파일 열린파일 = sistema_ng_file.buksan(pangalan);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = walang_laman_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int 읽기(int INDEX, byte[] 받을곳, int sukat_82232621) {
        서술자 pagpasok_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pagpasok_VALUE == null) {
            return -9;
        }
        if (sukat_82232621 < 0 || sukat_82232621 > 받을곳.length) {
            return -22;
        }
        int 남음 = pagpasok_VALUE.열린파일.data.length - pagpasok_VALUE.열린파일.posisyon;
        int 읽을크기 = Math.min(sukat_82232621, Math.max(남음, 0));
        System.arraycopy(pagpasok_VALUE.열린파일.data, pagpasok_VALUE.열린파일.posisyon, 받을곳, 0, 읽을크기);
        pagpasok_VALUE.열린파일.posisyon += 읽을크기;
        return 읽을크기;
    }

    public int ilipat_posisyon(int INDEX, int 거리, int Project_root) {
        서술자 pagpasok_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pagpasok_VALUE == null) {
            return -9;
        }
        int wallpaper_VALUE;
        if (Project_root == 0) {
            wallpaper_VALUE = 0;
        } else if (Project_root == 1) {
            wallpaper_VALUE = pagpasok_VALUE.열린파일.posisyon;
        } else if (Project_root == 2) {
            wallpaper_VALUE = pagpasok_VALUE.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = wallpaper_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        pagpasok_VALUE.열린파일.posisyon = 새위치;
        return 새위치;
    }

    public int isara(int INDEX) {
        서술자 pagpasok_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (pagpasok_VALUE == null) {
            return -9;
        }
        pagpasok_VALUE.열린파일.Sanggunian_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 pagpasok_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pagpasok_VALUE == null) {
            return -9;
        }
        int 새번호 = walang_laman_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        pagpasok_VALUE.열린파일.Sanggunian_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(pagpasok_VALUE.열린파일));
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
            isara(새번호);
        }
        원본.열린파일.Sanggunian_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 pagpasok_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pagpasok_VALUE == null) {
            return -9;
        }
        pagpasok_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 pagpasok_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pagpasok_VALUE == null) {
            return -9;
        }
        return pagpasok_VALUE.실행시닫기 ? 1 : 0;
    }

    public file_impormasyon msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new file_impormasyon(0, 0020666);
        }
        서술자 pagpasok_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (pagpasok_VALUE == null) {
            return null;
        }
        return new file_impormasyon(pagpasok_VALUE.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 pagpasok_VALUE = 서술자들.get(INDEX);
            if (pagpasok_VALUE != null && pagpasok_VALUE.실행시닫기) {
                isara(INDEX.intValue());
            }
        }
    }

    public boolean information_technology_buksan(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 sukat = new 파일서술자표(sistema_ng_file);
        for (Map.Entry<Integer, 서술자> pagpasok_VALUE : 서술자들.entrySet()) {
            pagpasok_VALUE.getValue().열린파일.Sanggunian_COUNT++;
            서술자 새서술자 = new 서술자(pagpasok_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = pagpasok_VALUE.getValue().실행시닫기;
            sukat.서술자들.put(pagpasok_VALUE.getKey(), 새서술자);
        }
        return sukat;
    }

    private int walang_laman_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
