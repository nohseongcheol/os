// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украіна.JUkrOS.файлавая_сістэма;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Файл 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final файлавая_сістэма.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(файлавая_сістэма.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final файлавая_сістэма файлавая_сістэма;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(файлавая_сістэма файлавая_сістэма) {
        this.файлавая_сістэма = файлавая_сістэма;
    }

    public int Адкрыць(String Назва) {
        файлавая_сістэма.열린파일 열린파일 = файлавая_сістэма.Адкрыць(Назва);
        if (열린파일 == null) {
            return -2;
        }
        int індэкс = нулявая_індэкс(3);
        if (індэкс < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(індэкс), new 서술자(열린파일));
        return індэкс;
    }

    public int Чытанне(int індэкс, byte[] 받을곳, int Памер) {
        서술자 увядзенне_значэнне = 서술자들.get(Integer.valueOf(індэкс));
        if (увядзенне_значэнне == null) {
            return -9;
        }
        if (Памер < 0 || Памер > 받을곳.length) {
            return -22;
        }
        int 남음 = увядзенне_значэнне.열린파일.дадзеныя.length - увядзенне_значэнне.열린파일.Пазіцыя;
        int 읽을크기 = Math.min(Памер, Math.max(남음, 0));
        System.arraycopy(увядзенне_значэнне.열린파일.дадзеныя, увядзенне_значэнне.열린파일.Пазіцыя, 받을곳, 0, 읽을크기);
        увядзенне_значэнне.열린파일.Пазіцыя += 읽을크기;
        return 읽을크기;
    }

    public int 위치옮기기(int індэкс, int 거리, int 기준) {
        서술자 увядзенне_значэнне = 서술자들.get(Integer.valueOf(індэкс));
        if (увядзенне_значэнне == null) {
            return -9;
        }
        int Фон_значэнне;
        if (기준 == 0) {
            Фон_значэнне = 0;
        } else if (기준 == 1) {
            Фон_значэнне = увядзенне_значэнне.열린파일.Пазіцыя;
        } else if (기준 == 2) {
            Фон_значэнне = увядзенне_значэнне.열린파일.дадзеныя.length;
        } else {
            return -22;
        }
        int 새위치 = Фон_значэнне + 거리;
        if (새위치 < 0) {
            return -22;
        }
        увядзенне_значэнне.열린파일.Пазіцыя = 새위치;
        return 새위치;
    }

    public int Закрыць(int індэкс) {
        서술자 увядзенне_значэнне = 서술자들.remove(Integer.valueOf(індэкс));
        if (увядзенне_значэнне == null) {
            return -9;
        }
        увядзенне_значэнне.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int індэкс, int 최소번호) {
        서술자 увядзенне_значэнне = 서술자들.get(Integer.valueOf(індэкс));
        if (увядзенне_значэнне == null) {
            return -9;
        }
        int 새번호 = нулявая_індэкс(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        увядзенне_значэнне.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(увядзенне_значэнне.열린파일));
        return 새번호;
    }

    public int 지정복제(int індэкс, int 새번호) {
        if (індэкс == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(індэкс)) ? індэкс : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(індэкс));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Закрыць(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int індэкс, boolean значэнне) {
        서술자 увядзенне_значэнне = 서술자들.get(Integer.valueOf(індэкс));
        if (увядзенне_значэнне == null) {
            return -9;
        }
        увядзенне_значэнне.실행시닫기 = значэнне;
        return 0;
    }

    public int 실행시닫기값(int індэкс) {
        서술자 увядзенне_значэнне = 서술자들.get(Integer.valueOf(індэкс));
        if (увядзенне_значэнне == null) {
            return -9;
        }
        return увядзенне_значэнне.실행시닫기 ? 1 : 0;
    }

    public файл_звесткі Сістэмная_інфармацыя(int індэкс) {
        if (індэкс >= 0 && індэкс <= 2) {
            return new файл_звесткі(0, 0020666);
        }
        서술자 увядзенне_значэнне = 서술자들.get(Integer.valueOf(індэкс));
        if (увядзенне_значэнне == null) {
            return null;
        }
        return new файл_звесткі(увядзенне_значэнне.열린파일.дадзеныя.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer індэкс : 번호들) {
            서술자 увядзенне_значэнне = 서술자들.get(індэкс);
            if (увядзенне_значэнне != null && увядзенне_значэнне.실행시닫기) {
                Закрыць(індэкс.intValue());
            }
        }
    }

    public boolean аддзел_інфармацыйных_тэхналогій_адкрыць(int індэкс) {
        return 서술자들.containsKey(Integer.valueOf(індэкс));
    }

    public 파일서술자표 복제() {
        파일서술자표 결과 = new 파일서술자표(файлавая_сістэма);
        for (Map.Entry<Integer, 서술자> увядзенне_значэнне : 서술자들.entrySet()) {
            увядзенне_значэнне.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(увядзенне_значэнне.getValue().열린파일);
            새서술자.실행시닫기 = увядзенне_значэнне.getValue().실행시닫기;
            결과.서술자들.put(увядзенне_значэнне.getKey(), 새서술자);
        }
        return 결과;
    }

    private int нулявая_індэкс(int 최소번호) {
        for (int індэкс = Math.max(0, 최소번호); індэкс < 최대서술자; індэкс++) {
            if (!서술자들.containsKey(Integer.valueOf(індэкс))) {
                return індэкс;
            }
        }
        return -1;
    }
}
