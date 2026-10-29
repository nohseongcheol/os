// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.фајл_систем;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Датотека 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final фајл_систем.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(фајл_систем.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final фајл_систем фајл_систем;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(фајл_систем фајл_систем) {
        this.фајл_систем = фајл_систем;
    }

    public int Отвори(String Назив) {
        фајл_систем.열린파일 열린파일 = фајл_систем.Отвори(Назив);
        if (열린파일 == null) {
            return -2;
        }
        int индекс = празно_индекс(3);
        if (индекс < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(индекс), new 서술자(열린파일));
        return индекс;
    }

    public int Чита(int индекс, byte[] 받을곳, int Величина) {
        서술자 унос_вриједност = 서술자들.get(Integer.valueOf(индекс));
        if (унос_вриједност == null) {
            return -9;
        }
        if (Величина < 0 || Величина > 받을곳.length) {
            return -22;
        }
        int 남음 = унос_вриједност.열린파일.подаци.length - унос_вриједност.열린파일.Положај;
        int 읽을크기 = Math.min(Величина, Math.max(남음, 0));
        System.arraycopy(унос_вриједност.열린파일.подаци, унос_вриједност.열린파일.Положај, 받을곳, 0, 읽을크기);
        унос_вриједност.열린파일.Положај += 읽을크기;
        return 읽을크기;
    }

    public int помаћи_позиција(int индекс, int 거리, int пројектовати_корен) {
        서술자 унос_вриједност = 서술자들.get(Integer.valueOf(индекс));
        if (унос_вриједност == null) {
            return -9;
        }
        int постер_вриједност;
        if (пројектовати_корен == 0) {
            постер_вриједност = 0;
        } else if (пројектовати_корен == 1) {
            постер_вриједност = унос_вриједност.열린파일.Положај;
        } else if (пројектовати_корен == 2) {
            постер_вриједност = унос_вриједност.열린파일.подаци.length;
        } else {
            return -22;
        }
        int 새위치 = постер_вриједност + 거리;
        if (새위치 < 0) {
            return -22;
        }
        унос_вриједност.열린파일.Положај = 새위치;
        return 새위치;
    }

    public int Затворен(int индекс) {
        서술자 унос_вриједност = 서술자들.remove(Integer.valueOf(индекс));
        if (унос_вриједност == null) {
            return -9;
        }
        унос_вриједност.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int индекс, int 최소번호) {
        서술자 унос_вриједност = 서술자들.get(Integer.valueOf(индекс));
        if (унос_вриједност == null) {
            return -9;
        }
        int 새번호 = празно_индекс(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        унос_вриједност.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(унос_вриједност.열린파일));
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
            Затворен(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int индекс, boolean вриједност) {
        서술자 унос_вриједност = 서술자들.get(Integer.valueOf(индекс));
        if (унос_вриједност == null) {
            return -9;
        }
        унос_вриједност.실행시닫기 = вриједност;
        return 0;
    }

    public int 실행시닫기값(int индекс) {
        서술자 унос_вриједност = 서술자들.get(Integer.valueOf(индекс));
        if (унос_вриједност == null) {
            return -9;
        }
        return унос_вриједност.실행시닫기 ? 1 : 0;
    }

    public фајл_информација Информације_о_систему(int индекс) {
        if (индекс >= 0 && индекс <= 2) {
            return new фајл_информација(0, 0020666);
        }
        서술자 унос_вриједност = 서술자들.get(Integer.valueOf(индекс));
        if (унос_вриједност == null) {
            return null;
        }
        return new фајл_информација(унос_вриједност.열린파일.подаци.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer индекс : 번호들) {
            서술자 унос_вриједност = 서술자들.get(индекс);
            if (унос_вриједност != null && унос_вриједност.실행시닫기) {
                Затворен(индекс.intValue());
            }
        }
    }

    public boolean информатичко_одељење_креирати(int индекс) {
        return 서술자들.containsKey(Integer.valueOf(индекс));
    }

    public 파일서술자표 клон_вриједност() {
        파일서술자표 ИСХОД = new 파일서술자표(фајл_систем);
        for (Map.Entry<Integer, 서술자> унос_вриједност : 서술자들.entrySet()) {
            унос_вриједност.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(унос_вриједност.getValue().열린파일);
            새서술자.실행시닫기 = унос_вриједност.getValue().실행시닫기;
            ИСХОД.서술자들.put(унос_вриједност.getKey(), 새서술자);
        }
        return ИСХОД;
    }

    private int празно_индекс(int 최소번호) {
        for (int индекс = Math.max(0, 최소번호); индекс < 최대서술자; индекс++) {
            if (!서술자들.containsKey(Integer.valueOf(индекс))) {
                return индекс;
            }
        }
        return -1;
    }
}
