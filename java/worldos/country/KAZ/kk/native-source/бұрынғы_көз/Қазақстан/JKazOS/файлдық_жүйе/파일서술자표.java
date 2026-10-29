// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.файлдық_жүйе;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Файл 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final файлдық_жүйе.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(файлдық_жүйе.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final файлдық_жүйе файлдық_жүйе;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(файлдық_жүйе файлдық_жүйе) {
        this.файлдық_жүйе = файлдық_жүйе;
    }

    public int Ашу(String Аты) {
        файлдық_жүйе.열린파일 열린파일 = файлдық_жүйе.Ашу(Аты);
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

    public int Оқу(int индекс, byte[] 받을곳, int Өлшемі) {
        서술자 енгізу_мән = 서술자들.get(Integer.valueOf(индекс));
        if (енгізу_мән == null) {
            return -9;
        }
        if (Өлшемі < 0 || Өлшемі > 받을곳.length) {
            return -22;
        }
        int 남음 = енгізу_мән.열린파일.деректер.length - енгізу_мән.열린파일.Орны;
        int 읽을크기 = Math.min(Өлшемі, Math.max(남음, 0));
        System.arraycopy(енгізу_мән.열린파일.деректер, енгізу_мән.열린파일.Орны, 받을곳, 0, 읽을크기);
        енгізу_мән.열린파일.Орны += 읽을크기;
        return 읽을크기;
    }

    public int жылжыту_лауазым(int индекс, int 거리, int жоба_түбір) {
        서술자 енгізу_мән = 서술자들.get(Integer.valueOf(индекс));
        if (енгізу_мән == null) {
            return -9;
        }
        int Фон_мән;
        if (жоба_түбір == 0) {
            Фон_мән = 0;
        } else if (жоба_түбір == 1) {
            Фон_мән = енгізу_мән.열린파일.Орны;
        } else if (жоба_түбір == 2) {
            Фон_мән = енгізу_мән.열린파일.деректер.length;
        } else {
            return -22;
        }
        int 새위치 = Фон_мән + 거리;
        if (새위치 < 0) {
            return -22;
        }
        енгізу_мән.열린파일.Орны = 새위치;
        return 새위치;
    }

    public int Жабу(int индекс) {
        서술자 енгізу_мән = 서술자들.remove(Integer.valueOf(индекс));
        if (енгізу_мән == null) {
            return -9;
        }
        енгізу_мән.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int индекс, int 최소번호) {
        서술자 енгізу_мән = 서술자들.get(Integer.valueOf(индекс));
        if (енгізу_мән == null) {
            return -9;
        }
        int Жаңа_нөмір = 빈번호(최소번호);
        if (Жаңа_нөмір < 0) {
            return -24;
        }
        енгізу_мән.열린파일.참조수++;
        서술자들.put(Integer.valueOf(Жаңа_нөмір), new 서술자(енгізу_мән.열린파일));
        return Жаңа_нөмір;
    }

    public int 지정복제(int индекс, int Жаңа_нөмір) {
        if (индекс == Жаңа_нөмір) {
            return 서술자들.containsKey(Integer.valueOf(индекс)) ? индекс : -9;
        }
        if (Жаңа_нөмір < 0 || Жаңа_нөмір >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(индекс));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Жаңа_нөмір))) {
            Жабу(Жаңа_нөмір);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(Жаңа_нөмір), new 서술자(원본.열린파일));
        return Жаңа_нөмір;
    }

    public int 실행시닫기설정(int индекс, boolean мән) {
        서술자 енгізу_мән = 서술자들.get(Integer.valueOf(индекс));
        if (енгізу_мән == null) {
            return -9;
        }
        енгізу_мән.실행시닫기 = мән;
        return 0;
    }

    public int 실행시닫기값(int индекс) {
        서술자 енгізу_мән = 서술자들.get(Integer.valueOf(индекс));
        if (енгізу_мән == null) {
            return -9;
        }
        return енгізу_мән.실행시닫기 ? 1 : 0;
    }

    public файл_ақпарат Жүйелік_ақпарат(int индекс) {
        if (индекс >= 0 && индекс <= 2) {
            return new файл_ақпарат(0, 0020666);
        }
        서술자 енгізу_мән = 서술자들.get(Integer.valueOf(индекс));
        if (енгізу_мән == null) {
            return null;
        }
        return new файл_ақпарат(енгізу_мән.열린파일.деректер.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer индекс : 번호들) {
            서술자 енгізу_мән = 서술자들.get(индекс);
            if (енгізу_мән != null && енгізу_мән.실행시닫기) {
                Жабу(индекс.intValue());
            }
        }
    }

    public boolean ақпараттық_жүйелер_ашу(int индекс) {
        return 서술자들.containsKey(Integer.valueOf(индекс));
    }

    public 파일서술자표 клон_мән() {
        파일서술자표 НӘТИЖЕ = new 파일서술자표(файлдық_жүйе);
        for (Map.Entry<Integer, 서술자> енгізу_мән : 서술자들.entrySet()) {
            енгізу_мән.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(енгізу_мән.getValue().열린파일);
            새서술자.실행시닫기 = енгізу_мән.getValue().실행시닫기;
            НӘТИЖЕ.서술자들.put(енгізу_мән.getKey(), 새서술자);
        }
        return НӘТИЖЕ;
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
