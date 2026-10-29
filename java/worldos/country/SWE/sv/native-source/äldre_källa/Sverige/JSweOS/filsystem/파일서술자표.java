// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sverige.JSweOS.filsystem;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 filnamn 설명을 유지한다. */
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

    public int Öppna(String Namn) {
        filsystem.열린파일 열린파일 = filsystem.Öppna(Namn);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = 빈번호(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Läs(int INDEX, byte[] få_mål, int Storlek) {
        서술자 post_värde = 서술자들.get(Integer.valueOf(INDEX));
        if (post_värde == null) {
            return -9;
        }
        if (Storlek < 0 || Storlek > få_mål.length) {
            return -22;
        }
        int 남음 = post_värde.열린파일.data.length - post_värde.열린파일.position;
        int läsa_storlek = Math.min(Storlek, Math.max(남음, 0));
        System.arraycopy(post_värde.열린파일.data, post_värde.열린파일.position, få_mål, 0, läsa_storlek);
        post_värde.열린파일.position += läsa_storlek;
        return läsa_storlek;
    }

    public int flytta_placera(int INDEX, int 거리, int åtgärd_rot) {
        서술자 post_värde = 서술자들.get(Integer.valueOf(INDEX));
        if (post_värde == null) {
            return -9;
        }
        int Bakgrund_värde;
        if (åtgärd_rot == 0) {
            Bakgrund_värde = 0;
        } else if (åtgärd_rot == 1) {
            Bakgrund_värde = post_värde.열린파일.position;
        } else if (åtgärd_rot == 2) {
            Bakgrund_värde = post_värde.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = Bakgrund_värde + 거리;
        if (새위치 < 0) {
            return -22;
        }
        post_värde.열린파일.position = 새위치;
        return 새위치;
    }

    public int Stäng(int INDEX) {
        서술자 post_värde = 서술자들.remove(Integer.valueOf(INDEX));
        if (post_värde == null) {
            return -9;
        }
        post_värde.열린파일.referens_ANTAL--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 post_värde = 서술자들.get(Integer.valueOf(INDEX));
        if (post_värde == null) {
            return -9;
        }
        int 새번호 = 빈번호(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        post_värde.열린파일.referens_ANTAL++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(post_värde.열린파일));
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
            Stäng(새번호);
        }
        원본.열린파일.referens_ANTAL++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean värde) {
        서술자 post_värde = 서술자들.get(Integer.valueOf(INDEX));
        if (post_värde == null) {
            return -9;
        }
        post_värde.실행시닫기 = värde;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 post_värde = 서술자들.get(Integer.valueOf(INDEX));
        if (post_värde == null) {
            return -9;
        }
        return post_värde.실행시닫기 ? 1 : 0;
    }

    public fil_info msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new fil_info(0, 0020666);
        }
        서술자 post_värde = 서술자들.get(Integer.valueOf(INDEX));
        if (post_värde == null) {
            return null;
        }
        return new fil_info(post_värde.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] nummer_ange = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : nummer_ange) {
            서술자 post_värde = 서술자들.get(INDEX);
            if (post_värde != null && post_värde.실행시닫기) {
                Stäng(INDEX.intValue());
            }
        }
    }

    public boolean informationsteknik_skapa(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 klon_värde() {
        파일서술자표 RESULTAT = new 파일서술자표(filsystem);
        for (Map.Entry<Integer, 서술자> post_värde : 서술자들.entrySet()) {
            post_värde.getValue().열린파일.referens_ANTAL++;
            서술자 새서술자 = new 서술자(post_värde.getValue().열린파일);
            새서술자.실행시닫기 = post_värde.getValue().실행시닫기;
            RESULTAT.서술자들.put(post_värde.getKey(), 새서술자);
        }
        return RESULTAT;
    }

    private int 빈번호(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
