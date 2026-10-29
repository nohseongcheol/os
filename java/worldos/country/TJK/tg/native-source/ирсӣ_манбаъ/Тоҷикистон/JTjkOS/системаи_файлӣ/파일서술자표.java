// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.системаи_файлӣ;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Файл 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final системаи_файлӣ.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(системаи_файлӣ.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final системаи_файлӣ системаи_файлӣ;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(системаи_файлӣ системаи_файлӣ) {
        this.системаи_файлӣ = системаи_файлӣ;
    }

    public int кушодан(String Ном) {
        системаи_файлӣ.열린파일 열린파일 = системаи_файлӣ.кушодан(Ном);
        if (열린파일 == null) {
            return -2;
        }
        int индекс = холӣ_индекс(3);
        if (индекс < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(индекс), new 서술자(열린파일));
        return индекс;
    }

    public int Хондан(int индекс, byte[] 받을곳, int андоза_кардан) {
        서술자 ворида_қимат = 서술자들.get(Integer.valueOf(индекс));
        if (ворида_қимат == null) {
            return -9;
        }
        if (андоза_кардан < 0 || андоза_кардан > 받을곳.length) {
            return -22;
        }
        int 남음 = ворида_қимат.열린파일.иттилоот.length - ворида_қимат.열린파일.위치;
        int 읽을크기 = Math.min(андоза_кардан, Math.max(남음, 0));
        System.arraycopy(ворида_қимат.열린파일.иттилоот, ворида_қимат.열린파일.위치, 받을곳, 0, 읽을크기);
        ворида_қимат.열린파일.위치 += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int индекс, int 거리, int 기준) {
        서술자 ворида_қимат = 서술자들.get(Integer.valueOf(индекс));
        if (ворида_қимат == null) {
            return -9;
        }
        int Пасзамина_қимат;
        if (기준 == 0) {
            Пасзамина_қимат = 0;
        } else if (기준 == 1) {
            Пасзамина_қимат = ворида_қимат.열린파일.위치;
        } else if (기준 == 2) {
            Пасзамина_қимат = ворида_қимат.열린파일.иттилоот.length;
        } else {
            return -22;
        }
        int 새위치 = Пасзамина_қимат + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ворида_қимат.열린파일.위치 = 새위치;
        return 새위치;
    }

    public int Пӯшидан(int индекс) {
        서술자 ворида_қимат = 서술자들.remove(Integer.valueOf(индекс));
        if (ворида_қимат == null) {
            return -9;
        }
        ворида_қимат.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int индекс, int 최소번호) {
        서술자 ворида_қимат = 서술자들.get(Integer.valueOf(индекс));
        if (ворида_қимат == null) {
            return -9;
        }
        int 새번호 = холӣ_индекс(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ворида_қимат.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ворида_қимат.열린파일));
        return 새번호;
    }

    public int 지정복제(int индекс, int 새번호) {
        if (индекс == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(индекс)) ? индекс : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(индекс));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Пӯшидан(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int индекс, boolean қимат) {
        서술자 ворида_қимат = 서술자들.get(Integer.valueOf(индекс));
        if (ворида_қимат == null) {
            return -9;
        }
        ворида_қимат.실행시닫기 = қимат;
        return 0;
    }

    public int 실행시닫기값(int индекс) {
        서술자 ворида_қимат = 서술자들.get(Integer.valueOf(индекс));
        if (ворида_қимат == null) {
            return -9;
        }
        return ворида_қимат.실행시닫기 ? 1 : 0;
    }

    public файл_маълумот Маълумоти_система(int индекс) {
        if (индекс >= 0 && индекс <= 2) {
            return new файл_маълумот(0, 0020666);
        }
        서술자 ворида_қимат = 서술자들.get(Integer.valueOf(индекс));
        if (ворида_қимат == null) {
            return null;
        }
        return new файл_маълумот(ворида_қимат.열린파일.иттилоот.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer индекс : 번호들) {
            서술자 ворида_қимат = 서술자들.get(индекс);
            if (ворида_қимат != null && ворида_қимат.실행시닫기) {
                Пӯшидан(индекс.intValue());
            }
        }
    }

    public boolean 열려있음(int индекс) {
        return 서술자들.containsKey(Integer.valueOf(индекс));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(системаи_файлӣ);
        for (Map.Entry<Integer, 서술자> ворида_қимат : 서술자들.entrySet()) {
            ворида_қимат.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ворида_қимат.getValue().열린파일);
            새서술자.실행시닫기 = ворида_қимат.getValue().실행시닫기;
            결과.서술자들.put(ворида_қимат.getKey(), 새서술자);
        }
        return 결과;
    }

    private int холӣ_индекс(int 최소번호) {
        for (int индекс = Math.max(0, 최소번호); индекс < 최대서술자; индекс++) {
            if (!서술자들.containsKey(Integer.valueOf(индекс))) {
                return индекс;
            }
        }
        return -1;
    }
}
