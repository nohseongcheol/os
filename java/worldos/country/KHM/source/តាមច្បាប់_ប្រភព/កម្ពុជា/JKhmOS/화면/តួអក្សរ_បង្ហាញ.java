// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class តួអក្សរ_បង្ហាញ {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int បញ្ឈរ_កំណត់ទីតាំង;

    public តួអក្សរ_បង្ហាញ() {
        លុប_ការបញ្ចូល();
    }

    public void លទ្ធផល(String មាតិកា_តំលៃ) {
        for (int សន្ទស្សន៏ = 0; សន្ទស្សន៏ < មាតិកា_តំលៃ.length(); សន្ទស្សន៏++) {
            char 문자 = មាតិកា_តំលៃ.charAt(សន្ទស្សន៏);
            if (문자 == '\n') {
                가로 = 0;
                បញ្ឈរ_កំណត់ទីតាំង++;
            } else {
                문자출력(가로++, បញ្ឈរ_កំណត់ទីតាំង, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                បញ្ឈរ_កំណត់ទីតាំង++;
            }
            if (បញ្ឈរ_កំណត់ទីតាំង >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int បញ្ឈរ_កំណត់ទីតាំង) {
        ផ្ទៀងផ្ទាត់_កំណត់ទីតាំង(가로, បញ្ឈរ_កំណត់ទីតាំង);
        return 문자들[បញ្ឈរ_កំណត់ទីតាំង * 너비 + 가로];
    }

    public void លុប_ការបញ្ចូល() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        បញ្ឈរ_កំណត់ទីតាំង = 0;
    }

    private void 문자출력(int 가로, int បញ្ឈរ_កំណត់ទីតាំង, char 문자) {
        ផ្ទៀងផ្ទាត់_កំណត់ទីតាំង(가로, បញ្ឈរ_កំណត់ទីតាំង);
        문자들[បញ្ឈរ_កំណត់ទីតាំង * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        បញ្ឈរ_កំណត់ទីតាំង = 높이 - 1;
    }

    private void ផ្ទៀងផ្ទាត់_កំណត់ទីតាំង(int 가로, int បញ្ឈរ_កំណត់ទីតាំង) {
        if (가로 < 0 || 가로 >= 너비 || បញ្ឈរ_កំណត់ទីតាំង < 0 || បញ្ឈរ_កំណត់ទីតាំង >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

