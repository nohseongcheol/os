// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.ឯកសារនៃប្រព័ន្ធ;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 ឯកសារ 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final ឯកសារនៃប្រព័ន្ធ.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(ឯកសារនៃប្រព័ន្ធ.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final ឯកសារនៃប្រព័ន្ធ ឯកសារនៃប្រព័ន្ធ;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(ឯកសារនៃប្រព័ន្ធ ឯកសារនៃប្រព័ន្ធ) {
        this.ឯកសារនៃប្រព័ន្ធ = ឯកសារនៃប្រព័ន្ធ;
    }

    public int បើក(String ឈ្មោះ) {
        ឯកសារនៃប្រព័ន្ធ.열린파일 열린파일 = ឯកសារនៃប្រព័ន្ធ.បើក(ឈ្មោះ);
        if (열린파일 == null) {
            return -2;
        }
        int សន្ទស្សន៏ = ទទេរ_សន្ទស្សន៏(3);
        if (សន្ទស្សន៏ < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(សន្ទស្សន៏), new 서술자(열린파일));
        return សន្ទស្សន៏;
    }

    public int អាន(int សន្ទស្សន៏, byte[] 받을곳, int ដាក់ទំហំ) {
        서술자 ការបញ្ចូល_តំលៃ = 서술자들.get(Integer.valueOf(សន្ទស្សន៏));
        if (ការបញ្ចូល_តំលៃ == null) {
            return -9;
        }
        if (ដាក់ទំហំ < 0 || ដាក់ទំហំ > 받을곳.length) {
            return -22;
        }
        int 남음 = ការបញ្ចូល_តំលៃ.열린파일.ទិន្នន័យ.length - ការបញ្ចូល_តំលៃ.열린파일.កំណត់ទីតាំង;
        int 읽을크기 = Math.min(ដាក់ទំហំ, Math.max(남음, 0));
        System.arraycopy(ការបញ្ចូល_តំលៃ.열린파일.ទិន្នន័យ, ការបញ្ចូល_តំលៃ.열린파일.កំណត់ទីតាំង, 받을곳, 0, 읽을크기);
        ការបញ្ចូល_តំលៃ.열린파일.កំណត់ទីតាំង += 읽을크기;
        return 읽을크기;
    }

    public int ផ្លាស់ទី_កំណត់ទីតាំង(int សន្ទស្សន៏, int 거리, int បញ្ចាំង_ឬស) {
        서술자 ការបញ្ចូល_តំលៃ = 서술자들.get(Integer.valueOf(សន្ទស្សន៏));
        if (ការបញ្ចូល_តំលៃ == null) {
            return -9;
        }
        int គំរូដែសថប_តំលៃ;
        if (បញ្ចាំង_ឬស == 0) {
            គំរូដែសថប_តំលៃ = 0;
        } else if (បញ្ចាំង_ឬស == 1) {
            គំរូដែសថប_តំលៃ = ការបញ្ចូល_តំលៃ.열린파일.កំណត់ទីតាំង;
        } else if (បញ្ចាំង_ឬស == 2) {
            គំរូដែសថប_តំលៃ = ការបញ្ចូល_តំលៃ.열린파일.ទិន្នន័យ.length;
        } else {
            return -22;
        }
        int 새위치 = គំរូដែសថប_តំលៃ + 거리;
        if (새위치 < 0) {
            return -22;
        }
        ការបញ្ចូល_តំលៃ.열린파일.កំណត់ទីតាំង = 새위치;
        return 새위치;
    }

    public int បិទ(int សន្ទស្សន៏) {
        서술자 ការបញ្ចូល_តំលៃ = 서술자들.remove(Integer.valueOf(សន្ទស្សន៏));
        if (ការបញ្ចូល_តំលៃ == null) {
            return -9;
        }
        ការបញ្ចូល_តំលៃ.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int សន្ទស្សន៏, int 최소번호) {
        서술자 ការបញ្ចូល_តំលៃ = 서술자들.get(Integer.valueOf(សន្ទស្សន៏));
        if (ការបញ្ចូល_តំលៃ == null) {
            return -9;
        }
        int 새번호 = ទទេរ_សន្ទស្សន៏(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        ការបញ្ចូល_តំលៃ.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(ការបញ្ចូល_តំលៃ.열린파일));
        return 새번호;
    }

    public int 지정복제(int សន្ទស្សន៏, int 새번호) {
        if (សន្ទស្សន៏ == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(សន្ទស្សន៏)) ? សន្ទស្សន៏ : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(សន្ទស្សន៏));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            បិទ(새번호);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int សន្ទស្សន៏, boolean តំលៃ) {
        서술자 ការបញ្ចូល_តំលៃ = 서술자들.get(Integer.valueOf(សន្ទស្សន៏));
        if (ការបញ្ចូល_តំលៃ == null) {
            return -9;
        }
        ការបញ្ចូល_តំលៃ.실행시닫기 = តំលៃ;
        return 0;
    }

    public int 실행시닫기값(int សន្ទស្សន៏) {
        서술자 ការបញ្ចូល_តំលៃ = 서술자들.get(Integer.valueOf(សន្ទស្សន៏));
        if (ការបញ្ចូល_តំលៃ == null) {
            return -9;
        }
        return ការបញ្ចូល_តំលៃ.실행시닫기 ? 1 : 0;
    }

    public ឯកសារ_ព័ត៌មាន ប្រព័ន្ធព័ត៌មាន(int សន្ទស្សន៏) {
        if (សន្ទស្សន៏ >= 0 && សន្ទស្សន៏ <= 2) {
            return new ឯកសារ_ព័ត៌មាន(0, 0020666);
        }
        서술자 ការបញ្ចូល_តំលៃ = 서술자들.get(Integer.valueOf(សន្ទស្សន៏));
        if (ការបញ្ចូល_តំលៃ == null) {
            return null;
        }
        return new ឯកសារ_ព័ត៌មាន(ការបញ្ចូល_តំលៃ.열린파일.ទិន្នន័យ.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer សន្ទស្សន៏ : 번호들) {
            서술자 ការបញ្ចូល_តំលៃ = 서술자들.get(សន្ទស្សន៏);
            if (ការបញ្ចូល_តំលៃ != null && ការបញ្ចូល_តំលៃ.실행시닫기) {
                បិទ(សន្ទស្សន៏.intValue());
            }
        }
    }

    public boolean បច្ចេកវិទ្យាព័ត៌មាន_បើក(int សន្ទស្សន៏) {
        return 서술자들.containsKey(Integer.valueOf(សន្ទស្សន៏));
    }

    public 파일서술자표 복제() {
        파일서술자표 ការវាស់វែង = new 파일서술자표(ឯកសារនៃប្រព័ន្ធ);
        for (Map.Entry<Integer, 서술자> ការបញ្ចូល_តំលៃ : 서술자들.entrySet()) {
            ការបញ្ចូល_តំលៃ.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(ការបញ្ចូល_តំលៃ.getValue().열린파일);
            새서술자.실행시닫기 = ការបញ្ចូល_តំលៃ.getValue().실행시닫기;
            ការវាស់វែង.서술자들.put(ការបញ្ចូល_តំលៃ.getKey(), 새서술자);
        }
        return ការវាស់វែង;
    }

    private int ទទេរ_សន្ទស្សន៏(int 최소번호) {
        for (int សន្ទស្សន៏ = Math.max(0, 최소번호); សន្ទស្សន៏ < 최대서술자; សន្ទស្សន៏++) {
            if (!서술자들.containsKey(Integer.valueOf(សន្ទស្សន៏))) {
                return សន្ទស្សន៏;
            }
        }
        return -1;
    }
}
