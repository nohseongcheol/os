// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.файл_системасы;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Birem 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final файл_системасы.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(файл_системасы.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final файл_системасы файл_системасы;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(файл_системасы файл_системасы) {
        this.файл_системасы = файл_системасы;
    }

    public int ачу(String исем) {
        файл_системасы.열린파일 열린파일 = файл_системасы.ачу(исем);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = Буш_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int 읽기(int INDEX, byte[] 받을곳, int үлчәмен_үзгәртү) {
        서술자 кертү_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (кертү_VALUE == null) {
            return -9;
        }
        if (үлчәмен_үзгәртү < 0 || үлчәмен_үзгәртү > 받을곳.length) {
            return -22;
        }
        int 남음 = кертү_VALUE.열린파일.мәгълүмат.length - кертү_VALUE.열린파일.урнаштыру;
        int 읽을크기 = Math.min(үлчәмен_үзгәртү, Math.max(남음, 0));
        System.arraycopy(кертү_VALUE.열린파일.мәгълүмат, кертү_VALUE.열린파일.урнаштыру, 받을곳, 0, 읽을크기);
        кертү_VALUE.열린파일.урнаштыру += 읽을크기;
        return 읽을크기;
    }

    public int күчерү_урнаштыру(int INDEX, int 거리, int экранга_җибәрү_тамыр) {
        서술자 кертү_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (кертү_VALUE == null) {
            return -9;
        }
        int Фон_VALUE;
        if (экранга_җибәрү_тамыр == 0) {
            Фон_VALUE = 0;
        } else if (экранга_җибәрү_тамыр == 1) {
            Фон_VALUE = кертү_VALUE.열린파일.урнаштыру;
        } else if (экранга_җибәрү_тамыр == 2) {
            Фон_VALUE = кертү_VALUE.열린파일.мәгълүмат.length;
        } else {
            return -22;
        }
        int 새위치 = Фон_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        кертү_VALUE.열린파일.урнаштыру = 새위치;
        return 새위치;
    }

    public int Yap(int INDEX) {
        서술자 кертү_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (кертү_VALUE == null) {
            return -9;
        }
        кертү_VALUE.열린파일.Белешмәлекләр_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 кертү_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (кертү_VALUE == null) {
            return -9;
        }
        int 새번호 = Буш_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        кертү_VALUE.열린파일.Белешмәлекләр_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(кертү_VALUE.열린파일));
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
            Yap(새번호);
        }
        원본.열린파일.Белешмәлекләр_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 кертү_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (кертү_VALUE == null) {
            return -9;
        }
        кертү_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 кертү_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (кертү_VALUE == null) {
            return -9;
        }
        return кертү_VALUE.실행시닫기 ? 1 : 0;
    }

    public файл_мәгълүмат msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new файл_мәгълүмат(0, 0020666);
        }
        서술자 кертү_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (кертү_VALUE == null) {
            return null;
        }
        return new файл_мәгълүмат(кертү_VALUE.열린파일.мәгълүмат.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 кертү_VALUE = 서술자들.get(INDEX);
            if (кертү_VALUE != null && кертү_VALUE.실행시닫기) {
                Yap(INDEX.intValue());
            }
        }
    }

    public boolean 열려있음(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 үлчәм = new 파일서술자표(файл_системасы);
        for (Map.Entry<Integer, 서술자> кертү_VALUE : 서술자들.entrySet()) {
            кертү_VALUE.getValue().열린파일.Белешмәлекләр_COUNT++;
            서술자 새서술자 = new 서술자(кертү_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = кертү_VALUE.getValue().실행시닫기;
            үлчәм.서술자들.put(кертү_VALUE.getKey(), 새서술자);
        }
        return үлчәм;
    }

    private int Буш_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
