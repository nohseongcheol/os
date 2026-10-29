// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украйна.JUkrOS.файлова_система;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Файл 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final файлова_система.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(файлова_система.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final файлова_система файлова_система;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(файлова_система файлова_система) {
        this.файлова_система = файлова_система;
    }

    public int Отваряне(String Име) {
        файлова_система.열린파일 열린파일 = файлова_система.Отваряне(Име);
        if (열린파일 == null) {
            return -2;
        }
        int индекс = 빈번호(3);
        if (индекс < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(индекс), new 서술자(열린파일));
        return индекс;
    }

    public int Четене(int индекс, byte[] получавам_местоназначение, int Размер) {
        서술자 запис_стойност = 서술자들.get(Integer.valueOf(индекс));
        if (запис_стойност == null) {
            return -9;
        }
        if (Размер < 0 || Размер > получавам_местоназначение.length) {
            return -22;
        }
        int 남음 = запис_стойност.열린파일.данни.length - запис_стойност.열린파일.Позиция;
        int 읽을크기 = Math.min(Размер, Math.max(남음, 0));
        System.arraycopy(запис_стойност.열린파일.данни, запис_стойност.열린파일.Позиция, получавам_местоназначение, 0, 읽을크기);
        запис_стойност.열린파일.Позиция += 읽을크기;
        return 읽을크기;
    }

    public int движа_се_позиция(int индекс, int 거리, int проект_корен) {
        서술자 запис_стойност = 서술자들.get(Integer.valueOf(индекс));
        if (запис_стойност == null) {
            return -9;
        }
        int Фон_стойност;
        if (проект_корен == 0) {
            Фон_стойност = 0;
        } else if (проект_корен == 1) {
            Фон_стойност = запис_стойност.열린파일.Позиция;
        } else if (проект_корен == 2) {
            Фон_стойност = запис_стойност.열린파일.данни.length;
        } else {
            return -22;
        }
        int 새위치 = Фон_стойност + 거리;
        if (새위치 < 0) {
            return -22;
        }
        запис_стойност.열린파일.Позиция = 새위치;
        return 새위치;
    }

    public int Затворен(int индекс) {
        서술자 запис_стойност = 서술자들.remove(Integer.valueOf(индекс));
        if (запис_стойност == null) {
            return -9;
        }
        запис_стойност.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int индекс, int 최소번호) {
        서술자 запис_стойност = 서술자들.get(Integer.valueOf(индекс));
        if (запис_стойност == null) {
            return -9;
        }
        int Нов_номер = 빈번호(최소번호);
        if (Нов_номер < 0) {
            return -24;
        }
        запис_стойност.열린파일.참조수++;
        서술자들.put(Integer.valueOf(Нов_номер), new 서술자(запис_стойност.열린파일));
        return Нов_номер;
    }

    public int 지정복제(int индекс, int Нов_номер) {
        if (индекс == Нов_номер) {
            return 서술자들.containsKey(Integer.valueOf(индекс)) ? индекс : -9;
        }
        if (Нов_номер < 0 || Нов_номер >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(индекс));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Нов_номер))) {
            Затворен(Нов_номер);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(Нов_номер), new 서술자(원본.열린파일));
        return Нов_номер;
    }

    public int 실행시닫기설정(int индекс, boolean стойност) {
        서술자 запис_стойност = 서술자들.get(Integer.valueOf(индекс));
        if (запис_стойност == null) {
            return -9;
        }
        запис_стойност.실행시닫기 = стойност;
        return 0;
    }

    public int 실행시닫기값(int индекс) {
        서술자 запис_стойност = 서술자들.get(Integer.valueOf(индекс));
        if (запис_стойност == null) {
            return -9;
        }
        return запис_стойност.실행시닫기 ? 1 : 0;
    }

    public Файл_инфо Системна_информация(int индекс) {
        if (индекс >= 0 && индекс <= 2) {
            return new Файл_инфо(0, 0020666);
        }
        서술자 запис_стойност = 서술자들.get(Integer.valueOf(индекс));
        if (запис_стойност == null) {
            return null;
        }
        return new Файл_инфо(запис_стойност.열린파일.данни.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer индекс : 번호들) {
            서술자 запис_стойност = 서술자들.get(индекс);
            if (запис_стойност != null && запис_стойност.실행시닫기) {
                Затворен(индекс.intValue());
            }
        }
    }

    public boolean информационни_технологии_отварям(int индекс) {
        return 서술자들.containsKey(Integer.valueOf(индекс));
    }

    public 파일서술자표 клонирам_стойност() {
        파일서술자표 РЕЗУЛТАТ = new 파일서술자표(файлова_система);
        for (Map.Entry<Integer, 서술자> запис_стойност : 서술자들.entrySet()) {
            запис_стойност.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(запис_стойност.getValue().열린파일);
            새서술자.실행시닫기 = запис_стойност.getValue().실행시닫기;
            РЕЗУЛТАТ.서술자들.put(запис_стойност.getKey(), 새서술자);
        }
        return РЕЗУЛТАТ;
    }

    private int 빈번호(int 최소번호) {
        for (int индекс = Math.max(0, 최소번호); индекс < 최대서술자; индекс++) {
            if (!서술자들.containsKey(Integer.valueOf(индекс))) {
                return индекс;
            }
        }
        return -1;
    }
}
