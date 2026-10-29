// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import ኢትዮጵያ.JEthOS.기억공간.ገጽ_አስተዳዳሪ;
import ኢትዮጵያ.JEthOS.የፋይል_ስርዓት.파일서술자표;

/** ሂደት_እሴት 식별자와 라운드로빈 አዘጋጅ_9ce364fc 대기열을 관리한다. */
public final class መርሀግብር_ኣውጭ {
    private final ገጽ_አስተዳዳሪ 쪽관리;
    private final Map<Integer, ሂደት_እሴት> የሂደት_ዝርዝር = new HashMap<Integer, ሂደት_እሴት>();
    private final Queue<ሂደት_እሴት> 준비대기열 = new ArrayDeque<ሂደት_እሴት>();
    private int ቀጣይ_መለያ = 1;

    public መርሀግብር_ኣውጭ(ገጽ_አስተዳዳሪ 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public ሂደት_እሴት 첫과정(파일서술자표 파일서술자) {
        ሂደት_እሴት 새과정 = new ሂደት_እሴት(መደብ_መለያ(), 0, 쪽관리.새주소공간(), 파일서술자);
        የሂደት_ዝርዝር.put(Integer.valueOf(새과정.መለያ_እሴት_5b7b8b77()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public ሂደት_እሴት 복제(ሂደት_እሴት 부모) {
        ሂደት_እሴት ልጅ_እሴት = new ሂደት_እሴት(
                መደብ_መለያ(),
                부모.መለያ_እሴት_5b7b8b77(),
                쪽관리.쓰기시복사복제(부모.አድራሻ_ቦታ()),
                부모.파일서술자().복제());
        ልጅ_እሴት.프로그램끝설정(부모.프로그램끝());
        የሂደት_ዝርዝር.put(Integer.valueOf(ልጅ_እሴት.መለያ_እሴት_5b7b8b77()), ልጅ_እሴት);
        준비대기열.offer(ልጅ_እሴት);
        return ልጅ_እሴት;
    }

    public ሂደት_እሴት ቀጣይ_ሂደት() {
        int 검사수 = 준비대기열.size();
        for (int መረጃ_ጠቆመ = 0; መረጃ_ጠቆመ < 검사수; መረጃ_ጠቆመ++) {
            ሂደት_እሴት ቀጣይ_ንጥል_ነገር = 준비대기열.poll();
            if (ቀጣይ_ንጥል_ነገር != null && (ቀጣይ_ንጥል_ነገር.ዞን_እሴት() == ሂደት_ዞን.አዘጋጅ_9ce364fc || ቀጣይ_ንጥል_ነገር.ዞን_እሴት() == ሂደት_ዞን.ፈጽም_ትእዛዝ)) {
                ቀጣይ_ንጥል_ነገር.ስብስብ_ዞን(ሂደት_ዞን.ፈጽም_ትእዛዝ);
                준비대기열.offer(ቀጣይ_ንጥል_ነገር);
                return ቀጣይ_ንጥል_ነገር;
            }
        }
        return null;
    }

    public int 자식기다리기(ሂደት_እሴት 부모, int ልጅ_መለያ, boolean 기다리지않음) {
        for (ሂደት_እሴት 후보 : የሂደት_ዝርዝር.values()) {
            if (후보.부모식별자() != 부모.መለያ_እሴት_5b7b8b77()) {
                continue;
            }
            if (ልጅ_መለያ > 0 && 후보.መለያ_እሴት_5b7b8b77() != ልጅ_መለያ) {
                continue;
            }
            if (후보.ዞን_እሴት() == ሂደት_ዞን.ውጣ_ፕሮግራም) {
                int ልኬት = (후보.종료값() & 0xff) << 8;
                የሂደት_ዝርዝር.remove(Integer.valueOf(후보.መለያ_እሴት_5b7b8b77()));
                return ልኬት;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public ሂደት_እሴት አግኝ_ሂደት(int መለያ_እሴት_5b7b8b77) {
        return የሂደት_ዝርዝር.get(Integer.valueOf(መለያ_እሴት_5b7b8b77));
    }

    private int መደብ_መለያ() {
        return ቀጣይ_መለያ++;
    }
}
