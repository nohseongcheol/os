// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkmaniston.JTkmOS.fayllar_tizimi;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fayl 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final fayllar_tizimi.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(fayllar_tizimi.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final fayllar_tizimi fayllar_tizimi;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(fayllar_tizimi fayllar_tizimi) {
        this.fayllar_tizimi = fayllar_tizimi;
    }

    public int Ochish(String Nomi) {
        fayllar_tizimi.열린파일 열린파일 = fayllar_tizimi.Ochish(Nomi);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = bo_sh_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Oʻqish(int INDEX, byte[] 받을곳, int Hajmi) {
        서술자 kiritish_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kiritish_VALUE == null) {
            return -9;
        }
        if (Hajmi < 0 || Hajmi > 받을곳.length) {
            return -22;
        }
        int 남음 = kiritish_VALUE.열린파일.ma_lumotlar.length - kiritish_VALUE.열린파일.Holati;
        int 읽을크기 = Math.min(Hajmi, Math.max(남음, 0));
        System.arraycopy(kiritish_VALUE.열린파일.ma_lumotlar, kiritish_VALUE.열린파일.Holati, 받을곳, 0, 읽을크기);
        kiritish_VALUE.열린파일.Holati += 읽을크기;
        return 읽을크기;
    }

    public int ko_chirmoq_holat(int INDEX, int 거리, int Project_ildiz) {
        서술자 kiritish_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kiritish_VALUE == null) {
            return -9;
        }
        int Fon_VALUE;
        if (Project_ildiz == 0) {
            Fon_VALUE = 0;
        } else if (Project_ildiz == 1) {
            Fon_VALUE = kiritish_VALUE.열린파일.Holati;
        } else if (Project_ildiz == 2) {
            Fon_VALUE = kiritish_VALUE.열린파일.ma_lumotlar.length;
        } else {
            return -22;
        }
        int 새위치 = Fon_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        kiritish_VALUE.열린파일.Holati = 새위치;
        return 새위치;
    }

    public int Yopish(int INDEX) {
        서술자 kiritish_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (kiritish_VALUE == null) {
            return -9;
        }
        kiritish_VALUE.열린파일.Ma_lumotnomalar_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 kiritish_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kiritish_VALUE == null) {
            return -9;
        }
        int 새번호 = bo_sh_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        kiritish_VALUE.열린파일.Ma_lumotnomalar_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(kiritish_VALUE.열린파일));
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
            Yopish(새번호);
        }
        원본.열린파일.Ma_lumotnomalar_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 kiritish_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kiritish_VALUE == null) {
            return -9;
        }
        kiritish_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 kiritish_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kiritish_VALUE == null) {
            return -9;
        }
        return kiritish_VALUE.실행시닫기 ? 1 : 0;
    }

    public fayl_ma_lumot msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new fayl_ma_lumot(0, 0020666);
        }
        서술자 kiritish_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (kiritish_VALUE == null) {
            return null;
        }
        return new fayl_ma_lumot(kiritish_VALUE.열린파일.ma_lumotlar.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 kiritish_VALUE = 서술자들.get(INDEX);
            if (kiritish_VALUE != null && kiritish_VALUE.실행시닫기) {
                Yopish(INDEX.intValue());
            }
        }
    }

    public boolean 열려있음(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 o_lchov = new 파일서술자표(fayllar_tizimi);
        for (Map.Entry<Integer, 서술자> kiritish_VALUE : 서술자들.entrySet()) {
            kiritish_VALUE.getValue().열린파일.Ma_lumotnomalar_COUNT++;
            서술자 새서술자 = new 서술자(kiritish_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = kiritish_VALUE.getValue().실행시닫기;
            o_lchov.서술자들.put(kiritish_VALUE.getKey(), 새서술자);
        }
        return o_lchov;
    }

    private int bo_sh_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
