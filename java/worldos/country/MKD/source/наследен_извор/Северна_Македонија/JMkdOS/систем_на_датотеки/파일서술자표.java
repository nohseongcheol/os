// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Северна_Македонија.JMkdOS.систем_на_датотеки;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Датотека 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final систем_на_датотеки.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(систем_на_датотеки.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final систем_на_датотеки систем_на_датотеки;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(систем_на_датотеки систем_на_датотеки) {
        this.систем_на_датотеки = систем_на_датотеки;
    }

    public int Отвори(String Име) {
        систем_на_датотеки.열린파일 열린파일 = систем_на_датотеки.Отвори(Име);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = празно_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Читај(int INDEX, byte[] 받을곳, int Големина) {
        서술자 внес_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (внес_VALUE == null) {
            return -9;
        }
        if (Големина < 0 || Големина > 받을곳.length) {
            return -22;
        }
        int 남음 = внес_VALUE.열린파일.податоци.length - внес_VALUE.열린파일.Позиција;
        int 읽을크기 = Math.min(Големина, Math.max(남음, 0));
        System.arraycopy(внес_VALUE.열린파일.податоци, внес_VALUE.열린파일.Позиција, 받을곳, 0, 읽을크기);
        внес_VALUE.열린파일.Позиција += 읽을크기;
        return 읽을크기;
    }

    public int премести_позиционирање(int INDEX, int 거리, int Project_корен) {
        서술자 внес_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (внес_VALUE == null) {
            return -9;
        }
        int тапет_VALUE;
        if (Project_корен == 0) {
            тапет_VALUE = 0;
        } else if (Project_корен == 1) {
            тапет_VALUE = внес_VALUE.열린파일.Позиција;
        } else if (Project_корен == 2) {
            тапет_VALUE = внес_VALUE.열린파일.податоци.length;
        } else {
            return -22;
        }
        int 새위치 = тапет_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        внес_VALUE.열린파일.Позиција = 새위치;
        return 새위치;
    }

    public int Затвори(int INDEX) {
        서술자 внес_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (внес_VALUE == null) {
            return -9;
        }
        внес_VALUE.열린파일.Референци_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 внес_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (внес_VALUE == null) {
            return -9;
        }
        int 새번호 = празно_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        внес_VALUE.열린파일.Референци_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(внес_VALUE.열린파일));
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
            Затвори(새번호);
        }
        원본.열린파일.Референци_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 внес_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (внес_VALUE == null) {
            return -9;
        }
        внес_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 внес_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (внес_VALUE == null) {
            return -9;
        }
        return внес_VALUE.실행시닫기 ? 1 : 0;
    }

    public датотека_информации msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new датотека_информации(0, 0020666);
        }
        서술자 внес_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (внес_VALUE == null) {
            return null;
        }
        return new датотека_информации(внес_VALUE.열린파일.податоци.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 внес_VALUE = 서술자들.get(INDEX);
            if (внес_VALUE != null && внес_VALUE.실행시닫기) {
                Затвори(INDEX.intValue());
            }
        }
    }

    public boolean информатичка_технологија_отвори(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 복제() {
        파일서술자표 мерка = new 파일서술자표(систем_на_датотеки);
        for (Map.Entry<Integer, 서술자> внес_VALUE : 서술자들.entrySet()) {
            внес_VALUE.getValue().열린파일.Референци_COUNT++;
            서술자 새서술자 = new 서술자(внес_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = внес_VALUE.getValue().실행시닫기;
            мерка.서술자들.put(внес_VALUE.getKey(), 새서술자);
        }
        return мерка;
    }

    private int празно_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
