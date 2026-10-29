// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Сербія.JSrbOS.файлова_система;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 файл 설명을 유지한다. */
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

    public int Відкрити(String Назва) {
        файлова_система.열린파일 열린파일 = файлова_система.Відкрити(Назва);
        if (열린파일 == null) {
            return -2;
        }
        int індекс = 빈번호(3);
        if (індекс < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(індекс), new 서술자(열린파일));
        return індекс;
    }

    public int Читання(int індекс, byte[] отримувати_місце, int Розмір) {
        서술자 запис_значення_962f286b = 서술자들.get(Integer.valueOf(індекс));
        if (запис_значення_962f286b == null) {
            return -9;
        }
        if (Розмір < 0 || Розмір > отримувати_місце.length) {
            return -22;
        }
        int 남음 = запис_значення_962f286b.열린파일.дані.length - запис_значення_962f286b.열린파일.позиція;
        int 읽을크기 = Math.min(Розмір, Math.max(남음, 0));
        System.arraycopy(запис_значення_962f286b.열린파일.дані, запис_значення_962f286b.열린파일.позиція, отримувати_місце, 0, 읽을크기);
        запис_значення_962f286b.열린파일.позиція += 읽을크기;
        return 읽을크기;
    }

    public int переміщати_посада(int індекс, int 거리, int Дії_корінь) {
        서술자 запис_значення_962f286b = 서술자들.get(Integer.valueOf(індекс));
        if (запис_значення_962f286b == null) {
            return -9;
        }
        int Фон_значення;
        if (Дії_корінь == 0) {
            Фон_значення = 0;
        } else if (Дії_корінь == 1) {
            Фон_значення = запис_значення_962f286b.열린파일.позиція;
        } else if (Дії_корінь == 2) {
            Фон_значення = запис_значення_962f286b.열린파일.дані.length;
        } else {
            return -22;
        }
        int 새위치 = Фон_значення + 거리;
        if (새위치 < 0) {
            return -22;
        }
        запис_значення_962f286b.열린파일.позиція = 새위치;
        return 새위치;
    }

    public int Закрити(int індекс) {
        서술자 запис_значення_962f286b = 서술자들.remove(Integer.valueOf(індекс));
        if (запис_значення_962f286b == null) {
            return -9;
        }
        запис_значення_962f286b.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int індекс, int 최소번호) {
        서술자 запис_значення_962f286b = 서술자들.get(Integer.valueOf(індекс));
        if (запис_значення_962f286b == null) {
            return -9;
        }
        int Додати_номер = 빈번호(최소번호);
        if (Додати_номер < 0) {
            return -24;
        }
        запис_значення_962f286b.열린파일.참조수++;
        서술자들.put(Integer.valueOf(Додати_номер), new 서술자(запис_значення_962f286b.열린파일));
        return Додати_номер;
    }

    public int 지정복제(int індекс, int Додати_номер) {
        if (індекс == Додати_номер) {
            return 서술자들.containsKey(Integer.valueOf(індекс)) ? індекс : -9;
        }
        if (Додати_номер < 0 || Додати_номер >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(індекс));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Додати_номер))) {
            Закрити(Додати_номер);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(Додати_номер), new 서술자(원본.열린파일));
        return Додати_номер;
    }

    public int 실행시닫기설정(int індекс, boolean значення) {
        서술자 запис_значення_962f286b = 서술자들.get(Integer.valueOf(індекс));
        if (запис_значення_962f286b == null) {
            return -9;
        }
        запис_значення_962f286b.실행시닫기 = значення;
        return 0;
    }

    public int 실행시닫기값(int індекс) {
        서술자 запис_значення_962f286b = 서술자들.get(Integer.valueOf(індекс));
        if (запис_значення_962f286b == null) {
            return -9;
        }
        return запис_значення_962f286b.실행시닫기 ? 1 : 0;
    }

    public Файл_відомості Відомості_про_систему(int індекс) {
        if (індекс >= 0 && індекс <= 2) {
            return new Файл_відомості(0, 0020666);
        }
        서술자 запис_значення_962f286b = 서술자들.get(Integer.valueOf(індекс));
        if (запис_значення_962f286b == null) {
            return null;
        }
        return new Файл_відомості(запис_значення_962f286b.열린파일.дані.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer індекс : 번호들) {
            서술자 запис_значення_962f286b = 서술자들.get(індекс);
            if (запис_значення_962f286b != null && запис_значення_962f286b.실행시닫기) {
                Закрити(індекс.intValue());
            }
        }
    }

    public boolean ІТ_відділ_відкрито(int індекс) {
        return 서술자들.containsKey(Integer.valueOf(індекс));
    }

    public 파일서술자표 клонувати_значення() {
        파일서술자표 результат = new 파일서술자표(файлова_система);
        for (Map.Entry<Integer, 서술자> запис_значення_962f286b : 서술자들.entrySet()) {
            запис_значення_962f286b.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(запис_значення_962f286b.getValue().열린파일);
            새서술자.실행시닫기 = запис_значення_962f286b.getValue().실행시닫기;
            результат.서술자들.put(запис_значення_962f286b.getKey(), 새서술자);
        }
        return результат;
    }

    private int 빈번호(int 최소번호) {
        for (int індекс = Math.max(0, 최소번호); індекс < 최대서술자; індекс++) {
            if (!서술자들.containsKey(Integer.valueOf(індекс))) {
                return індекс;
            }
        }
        return -1;
    }
}
