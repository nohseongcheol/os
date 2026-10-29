// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ირანი.JIrnOS.ფაილური_სისტემა;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ფაილი 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ფაილური_სისტემა.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ფაილური_სისტემა.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ფაილური_სისტემა ფაილური_სისტემა;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ფაილური_სისტემა ფაილური_სისტემა) {
        this.ფაილური_სისტემა = ფაილური_სისტემა;
    }

    public int გახსნა(String სახელი) {
        ფაილური_სისტემა.열린파일 열린파일 = ფაილური_სისტემა.გახსნა(სახელი);
        if (열린파일 == null) {
            return -2;
        }
        int ინდექსი = ცარიელი_ინდექსი(3);
        if (ინდექსი < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(ინდექსი), new 서술자(열린파일));
        return ინდექსი;
    }

    public int კითხვა(int ინდექსი, byte[] 받을곳, int ზომა) {
        서술자 შენატანი_მნიშვნელობა = 서술자들.get(Integer.valueOf(ინდექსი));
        if (შენატანი_მნიშვნელობა == null) {
            return -9;
        }
        if (ზომა < 0 || ზომა > 받을곳.length) {
            return -22;
        }
        int 남음 = შენატანი_მნიშვნელობა.열린파일.მონაცემები.length - შენატანი_მნიშვნელობა.열린파일.პოზიცია;
        int 읽을크기 = Math.min(ზომა, Math.max(남음, 0));
        System.arraycopy(შენატანი_მნიშვნელობა.열린파일.მონაცემები, შენატანი_მნიშვნელობა.열린파일.პოზიცია, 받을곳, 0, 읽을크기);
        შენატანი_მნიშვნელობა.열린파일.პოზიცია += 읽을크기;
        return 읽을크기;
    }

    public int გადატანა_პოზიცია(int ინდექსი, int 거리, int პროეცირება_ფესვი) {
        서술자 შენატანი_მნიშვნელობა = 서술자들.get(Integer.valueOf(ინდექსი));
        if (შენატანი_მნიშვნელობა == null) {
            return -9;
        }
        int ფონი_მნიშვნელობა;
        if (პროეცირება_ფესვი == 0) {
            ფონი_მნიშვნელობა = 0;
        } else if (პროეცირება_ფესვი == 1) {
            ფონი_მნიშვნელობა = შენატანი_მნიშვნელობა.열린파일.პოზიცია;
        } else if (პროეცირება_ფესვი == 2) {
            ფონი_მნიშვნელობა = შენატანი_მნიშვნელობა.열린파일.მონაცემები.length;
        } else {
            return -22;
        }
        int 새위치 = ფონი_მნიშვნელობა + 거리;
        if (새위치 < 0) {
            return -22;
        }
        შენატანი_მნიშვნელობა.열린파일.პოზიცია = 새위치;
        return 새위치;
    }

    public int დახურვა(int ინდექსი) {
        서술자 შენატანი_მნიშვნელობა = 서술자들.remove(Integer.valueOf(ინდექსი));
        if (შენატანი_მნიშვნელობა == null) {
            return -9;
        }
        შენატანი_მნიშვნელობა.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int ინდექსი, int 최소번호) {
        서술자 შენატანი_მნიშვნელობა = 서술자들.get(Integer.valueOf(ინდექსი));
        if (შენატანი_მნიშვნელობა == null) {
            return -9;
        }
        int 새번호 = ცარიელი_ინდექსი(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        შენატანი_მნიშვნელობა.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(შენატანი_მნიშვნელობა.열린파일));
        return 새번호;
    }

    public int 지정복제(int ინდექსი, int 새번호) {
        if (ინდექსი == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(ინდექსი)) ? ინდექსი : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(ინდექსი));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            დახურვა(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int ინდექსი, boolean მნიშვნელობა) {
        서술자 შენატანი_მნიშვნელობა = 서술자들.get(Integer.valueOf(ინდექსი));
        if (შენატანი_მნიშვნელობა == null) {
            return -9;
        }
        შენატანი_მნიშვნელობა.실행시닫기 = მნიშვნელობა;
        return 0;
    }

    public int 실행시닫기값(int ინდექსი) {
        서술자 შენატანი_მნიშვნელობა = 서술자들.get(Integer.valueOf(ინდექსი));
        if (შენატანი_მნიშვნელობა == null) {
            return -9;
        }
        return შენატანი_მნიშვნელობა.실행시닫기 ? 1 : 0;
    }

    public ფაილი_ინფო სისტემის_ინფორმაცია(int ინდექსი) {
        if (ინდექსი >= 0 && ინდექსი <= 2) {
            return new ფაილი_ინფო(0, 0020666);
        }
        서술자 შენატანი_მნიშვნელობა = 서술자들.get(Integer.valueOf(ინდექსი));
        if (შენატანი_მნიშვნელობა == null) {
            return null;
        }
        return new ფაილი_ინფო(შენატანი_მნიშვნელობა.열린파일.მონაცემები.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer ინდექსი : 번호들) {
            서술자 შენატანი_მნიშვნელობა = 서술자들.get(ინდექსი);
            if (შენატანი_მნიშვნელობა != null && შენატანი_მნიშვნელობა.실행시닫기) {
                დახურვა(ინდექსი.intValue());
            }
        }
    }

    public boolean 열려있음(int ინდექსი) {
        return 서술자들.containsKey(Integer.valueOf(ინდექსი));
    }

    public 파일서술자표 복제() {
        파일서술자표 გაზომვა = new 파일서술자표(ფაილური_სისტემა);
        for (Map.Entry<Integer, 서술자> შენატანი_მნიშვნელობა : 서술자들.entrySet()) {
            შენატანი_მნიშვნელობა.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(შენატანი_მნიშვნელობა.getValue().열린파일);
            새서술자.실행시닫기 = შენატანი_მნიშვნელობა.getValue().실행시닫기;
            გაზომვა.서술자들.put(შენატანი_მნიშვნელობა.getKey(), 새서술자);
        }
        return გაზომვა;
    }

    private int ცარიელი_ინდექსი(int 최소번호) {
        for (int ინდექსი = Math.max(0, 최소번호); ინდექსი < 최대서술자; ინდექსი++) {
            if (!서술자들.containsKey(Integer.valueOf(ინდექსი))) {
                return ინდექსი;
            }
        }
        return -1;
    }
}
