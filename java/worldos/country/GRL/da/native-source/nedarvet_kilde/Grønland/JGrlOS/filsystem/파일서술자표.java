// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Grønland.JGrlOS.filsystem;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Fil 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final filsystem.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(filsystem.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final filsystem filsystem;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(filsystem filsystem) {
        this.filsystem = filsystem;
    }

    public int Åbn(String Navn) {
        filsystem.열린파일 열린파일 = filsystem.Åbn(Navn);
        if (열린파일 == null) {
            return -2;
        }
        int INDEKS = 빈번호(3);
        if (INDEKS < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEKS), new 서술자(열린파일));
        return INDEKS;
    }

    public int Læse(int INDEKS, byte[] modtage_destination, int Størrelse) {
        서술자 post_VÆRDI_962f286b = 서술자들.get(Integer.valueOf(INDEKS));
        if (post_VÆRDI_962f286b == null) {
            return -9;
        }
        if (Størrelse < 0 || Størrelse > modtage_destination.length) {
            return -22;
        }
        int 남음 = post_VÆRDI_962f286b.열린파일.data.length - post_VÆRDI_962f286b.열린파일.Placering;
        int 읽을크기 = Math.min(Størrelse, Math.max(남음, 0));
        System.arraycopy(post_VÆRDI_962f286b.열린파일.data, post_VÆRDI_962f286b.열린파일.Placering, modtage_destination, 0, 읽을크기);
        post_VÆRDI_962f286b.열린파일.Placering += 읽을크기;
        return 읽을크기;
    }

    public int flytte_placere(int INDEKS, int 거리, int To_do_rod) {
        서술자 post_VÆRDI_962f286b = 서술자들.get(Integer.valueOf(INDEKS));
        if (post_VÆRDI_962f286b == null) {
            return -9;
        }
        int Baggrund_VÆRDI;
        if (To_do_rod == 0) {
            Baggrund_VÆRDI = 0;
        } else if (To_do_rod == 1) {
            Baggrund_VÆRDI = post_VÆRDI_962f286b.열린파일.Placering;
        } else if (To_do_rod == 2) {
            Baggrund_VÆRDI = post_VÆRDI_962f286b.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = Baggrund_VÆRDI + 거리;
        if (새위치 < 0) {
            return -22;
        }
        post_VÆRDI_962f286b.열린파일.Placering = 새위치;
        return 새위치;
    }

    public int Luk(int INDEKS) {
        서술자 post_VÆRDI_962f286b = 서술자들.remove(Integer.valueOf(INDEKS));
        if (post_VÆRDI_962f286b == null) {
            return -9;
        }
        post_VÆRDI_962f286b.열린파일.referere_TÆL--;
        return 0;
    }

    public int 복제서술자(int INDEKS, int 최소번호) {
        서술자 post_VÆRDI_962f286b = 서술자들.get(Integer.valueOf(INDEKS));
        if (post_VÆRDI_962f286b == null) {
            return -9;
        }
        int Nyt_nummer = 빈번호(최소번호);
        if (Nyt_nummer < 0) {
            return -24;
        }
        post_VÆRDI_962f286b.열린파일.referere_TÆL++;
        서술자들.put(Integer.valueOf(Nyt_nummer), new 서술자(post_VÆRDI_962f286b.열린파일));
        return Nyt_nummer;
    }

    public int 지정복제(int INDEKS, int Nyt_nummer) {
        if (INDEKS == Nyt_nummer) {
            return 서술자들.containsKey(Integer.valueOf(INDEKS)) ? INDEKS : -9;
        }
        if (Nyt_nummer < 0 || Nyt_nummer >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEKS));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Nyt_nummer))) {
            Luk(Nyt_nummer);
        }
        원본.열린파일.referere_TÆL++;
        서술자들.put(Integer.valueOf(Nyt_nummer), new 서술자(원본.열린파일));
        return Nyt_nummer;
    }

    public int 실행시닫기설정(int INDEKS, boolean VÆRDI) {
        서술자 post_VÆRDI_962f286b = 서술자들.get(Integer.valueOf(INDEKS));
        if (post_VÆRDI_962f286b == null) {
            return -9;
        }
        post_VÆRDI_962f286b.실행시닫기 = VÆRDI;
        return 0;
    }

    public int 실행시닫기값(int INDEKS) {
        서술자 post_VÆRDI_962f286b = 서술자들.get(Integer.valueOf(INDEKS));
        if (post_VÆRDI_962f286b == null) {
            return -9;
        }
        return post_VÆRDI_962f286b.실행시닫기 ? 1 : 0;
    }

    public fil_info msinfo32_exe(int INDEKS) {
        if (INDEKS >= 0 && INDEKS <= 2) {
            return new fil_info(0, 0020666);
        }
        서술자 post_VÆRDI_962f286b = 서술자들.get(Integer.valueOf(INDEKS));
        if (post_VÆRDI_962f286b == null) {
            return null;
        }
        return new fil_info(post_VÆRDI_962f286b.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] tal_Liste = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEKS : tal_Liste) {
            서술자 post_VÆRDI_962f286b = 서술자들.get(INDEKS);
            if (post_VÆRDI_962f286b != null && post_VÆRDI_962f286b.실행시닫기) {
                Luk(INDEKS.intValue());
            }
        }
    }

    public boolean it_åben(int INDEKS) {
        return 서술자들.containsKey(Integer.valueOf(INDEKS));
    }

    public 파일서술자표 klon_VÆRDI() {
        파일서술자표 KR = new 파일서술자표(filsystem);
        for (Map.Entry<Integer, 서술자> post_VÆRDI_962f286b : 서술자들.entrySet()) {
            post_VÆRDI_962f286b.getValue().열린파일.referere_TÆL++;
            서술자 새서술자 = new 서술자(post_VÆRDI_962f286b.getValue().열린파일);
            새서술자.실행시닫기 = post_VÆRDI_962f286b.getValue().실행시닫기;
            KR.서술자들.put(post_VÆRDI_962f286b.getKey(), 새서술자);
        }
        return KR;
    }

    private int 빈번호(int 최소번호) {
        for (int INDEKS = Math.max(0, 최소번호); INDEKS < 최대서술자; INDEKS++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEKS))) {
                return INDEKS;
            }
        }
        return -1;
    }
}
