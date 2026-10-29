// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.файл_тутуму;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Файл 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final файл_тутуму.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(файл_тутуму.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final файл_тутуму файл_тутуму;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(файл_тутуму файл_тутуму) {
        this.файл_тутуму = файл_тутуму;
    }

    public int Ачуу(String Аты) {
        файл_тутуму.열린파일 열린파일 = файл_тутуму.Ачуу(Аты);
        if (열린파일 == null) {
            return -2;
        }
        int индекс = бош_индекс(3);
        if (индекс < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(индекс), new 서술자(열린파일));
        return индекс;
    }

    public int Окуу(int индекс, byte[] 받을곳, int Өлчөмү) {
        서술자 киргизме_жазуу_маани = 서술자들.get(Integer.valueOf(индекс));
        if (киргизме_жазуу_маани == null) {
            return -9;
        }
        if (Өлчөмү < 0 || Өлчөмү > 받을곳.length) {
            return -22;
        }
        int 남음 = киргизме_жазуу_маани.열린파일.берилмелер.length - киргизме_жазуу_маани.열린파일.Турган_жери;
        int 읽을크기 = Math.min(Өлчөмү, Math.max(남음, 0));
        System.arraycopy(киргизме_жазуу_маани.열린파일.берилмелер, киргизме_жазуу_маани.열린파일.Турган_жери, 받을곳, 0, 읽을크기);
        киргизме_жазуу_маани.열린파일.Турган_жери += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int индекс, int 거리, int 기준) {
        서술자 киргизме_жазуу_маани = 서술자들.get(Integer.valueOf(индекс));
        if (киргизме_жазуу_маани == null) {
            return -9;
        }
        int Фон_маани;
        if (기준 == 0) {
            Фон_маани = 0;
        } else if (기준 == 1) {
            Фон_маани = киргизме_жазуу_маани.열린파일.Турган_жери;
        } else if (기준 == 2) {
            Фон_маани = киргизме_жазуу_маани.열린파일.берилмелер.length;
        } else {
            return -22;
        }
        int 새위치 = Фон_маани + 거리;
        if (새위치 < 0) {
            return -22;
        }
        киргизме_жазуу_маани.열린파일.Турган_жери = 새위치;
        return 새위치;
    }

    public int Жабуу(int индекс) {
        서술자 киргизме_жазуу_маани = 서술자들.remove(Integer.valueOf(индекс));
        if (киргизме_жазуу_маани == null) {
            return -9;
        }
        киргизме_жазуу_маани.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int индекс, int 최소번호) {
        서술자 киргизме_жазуу_маани = 서술자들.get(Integer.valueOf(индекс));
        if (киргизме_жазуу_маани == null) {
            return -9;
        }
        int 새번호 = бош_индекс(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        киргизме_жазуу_маани.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(киргизме_жазуу_маани.열린파일));
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
            Жабуу(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int индекс, boolean маани) {
        서술자 киргизме_жазуу_маани = 서술자들.get(Integer.valueOf(индекс));
        if (киргизме_жазуу_маани == null) {
            return -9;
        }
        киргизме_жазуу_маани.실행시닫기 = маани;
        return 0;
    }

    public int 실행시닫기값(int индекс) {
        서술자 киргизме_жазуу_маани = 서술자들.get(Integer.valueOf(индекс));
        if (киргизме_жазуу_маани == null) {
            return -9;
        }
        return киргизме_жазуу_маани.실행시닫기 ? 1 : 0;
    }

    public файл_маалымат Система_маалыматы(int индекс) {
        if (индекс >= 0 && индекс <= 2) {
            return new файл_маалымат(0, 0020666);
        }
        서술자 киргизме_жазуу_маани = 서술자들.get(Integer.valueOf(индекс));
        if (киргизме_жазуу_маани == null) {
            return null;
        }
        return new файл_маалымат(киргизме_жазуу_маани.열린파일.берилмелер.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer индекс : 번호들) {
            서술자 киргизме_жазуу_маани = 서술자들.get(индекс);
            if (киргизме_жазуу_маани != null && киргизме_жазуу_маани.실행시닫기) {
                Жабуу(индекс.intValue());
            }
        }
    }

    public boolean 열려있음(int индекс) {
        return 서술자들.containsKey(Integer.valueOf(индекс));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(файл_тутуму);
        for (Map.Entry<Integer, 서술자> киргизме_жазуу_маани : 서술자들.entrySet()) {
            киргизме_жазуу_маани.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(киргизме_жазуу_маани.getValue().열린파일);
            새서술자.실행시닫기 = киргизме_жазуу_маани.getValue().실행시닫기;
            결과.서술자들.put(киргизме_жазуу_маани.getKey(), 새서술자);
        }
        return 결과;
    }

    private int бош_индекс(int 최소번호) {
        for (int индекс = Math.max(0, 최소번호); индекс < 최대서술자; индекс++) {
            if (!서술자들.containsKey(Integer.valueOf(индекс))) {
                return индекс;
            }
        }
        return -1;
    }
}
