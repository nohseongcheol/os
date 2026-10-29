// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package নেপাল.JNplOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB পৃষ্ঠা_মান 연결과 লেখা 시 복사를 제공한다. */
public final class পৃষ্ঠা_ব্যবস্থাপক {
    public static final int পৃষ্ঠার_মাপ = 4096;

    private static final class পৃষ্ঠা_মান {
        private byte[] ডাটা = new byte[পৃষ্ঠার_মাপ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ইমেইল_স্পেস {
        private final Map<Integer, পৃষ্ঠা_মান> পৃষ্ঠা_সারণি = new HashMap<Integer, পৃষ্ঠা_মান>();
    }

    public ইমেইল_স্পেস 새주소공간() {
        return new ইমেইল_স্পেস();
    }

    public void ম্যাপ_পৃষ্ঠা(ইমেইল_স্পেস 공간, int ভার্চুয়াল_ঠিকানা, boolean 쓰기가능) {
        int সূচি = 쪽번호(ভার্চুয়াল_ঠিকানা);
        পৃষ্ঠা_মান 새쪽 = new পৃষ্ঠা_মান();
        새쪽.쓰기가능 = 쓰기가능;
        공간.পৃষ্ঠা_সারণি.put(Integer.valueOf(সূচি), 새쪽);
    }

    public ইমেইল_স্পেস 쓰기시복사복제(ইমেইল_স্পেস 원본) {
        ইমেইল_স্পেস 복제본 = new ইমেইল_স্পেস();
        for (Map.Entry<Integer, পৃষ্ঠা_মান> ভুক্তি_মান : 원본.পৃষ্ঠা_সারণি.entrySet()) {
            পৃষ্ঠা_মান 공유쪽 = ভুক্তি_মান.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.পৃষ্ঠা_সারণি.put(ভুক্তি_মান.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ইমেইল_স্পেস 공간, int ভার্চুয়াল_ঠিকানা) {
        পৃষ্ঠা_মান লক্ষ্য = খোঁজা_পৃষ্ঠা(공간, ভার্চুয়াল_ঠিকানা);
        return লক্ষ্য.ডাটা[Math.floorMod(ভার্চুয়াল_ঠিকানা, পৃষ্ঠার_মাপ)];
    }

    public void লেখা_বাইট_মান(ইমেইল_স্পেস 공간, int ভার্চুয়াল_ঠিকানা, byte মান) {
        int সূচি = 쪽번호(ভার্চুয়াল_ঠিকানা);
        পৃষ্ঠা_মান লক্ষ্য = খোঁজা_পৃষ্ঠা(공간, ভার্চুয়াল_ঠিকানা);
        if (!লক্ষ্য.쓰기가능) {
            if (!লক্ষ্য.쓰기시복사) {
                throw new IllegalStateException("পড়া 전용 쪽입니다.");
            }
            লক্ষ্য = ক্রিয়েট_নিজস্ব_পৃষ্ঠা(공간, সূচি, লক্ষ্য);
        }
        লক্ষ্য.ডাটা[Math.floorMod(ভার্চুয়াল_ঠিকানা, পৃষ্ঠার_মাপ)] = মান;
    }

    public void 범위개인쓰기(ইমেইল_স্পেস 공간, int শুরু_ইমেইল, int আকার) {
        if (আকার < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int শেষ_করা_ইমেইল = Math.addExact(শুরু_ইমেইল, আকার);
        for (int ইমেইল = শুরু_ইমেইল; ইমেইল < শেষ_করা_ইমেইল; ইমেইল = (쪽번호(ইমেইল) + 1) * পৃষ্ঠার_মাপ) {
            int সূচি = 쪽번호(ইমেইল);
            পৃষ্ঠা_মান লক্ষ্য = খোঁজা_পৃষ্ঠা(공간, ইমেইল);
            if (লক্ষ্য.쓰기시복사) {
                ক্রিয়েট_নিজস্ব_পৃষ্ঠা(공간, সূচি, লক্ষ্য);
            } else {
                লক্ষ্য.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ইমেইল_স্পেস 공간, int শুরু_ইমেইল, byte[] ডাটা) {
        for (int সূচি = 0; সূচি < ডাটা.length; সূচি++) {
            লেখা_বাইট_মান(공간, শুরু_ইমেইল + সূচি, ডাটা[সূচি]);
        }
    }

    private পৃষ্ঠা_মান ক্রিয়েট_নিজস্ব_পৃষ্ঠা(ইমেইল_স্পেস 공간, int সূচি, পৃষ্ঠা_মান 공유쪽) {
        পৃষ্ঠা_মান নিজস্ব_পৃষ্ঠা = new পৃষ্ঠা_মান();
        নিজস্ব_পৃষ্ঠা.ডাটা = Arrays.copyOf(공유쪽.ডাটা, 공유쪽.ডাটা.length);
        নিজস্ব_পৃষ্ঠা.쓰기가능 = true;
        নিজস্ব_পৃষ্ঠা.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.পৃষ্ঠা_সারণি.put(Integer.valueOf(সূচি), নিজস্ব_পৃষ্ঠা);
        return নিজস্ব_পৃষ্ঠা;
    }

    private পৃষ্ঠা_মান খোঁজা_পৃষ্ঠা(ইমেইল_স্পেস 공간, int ইমেইল) {
        পৃষ্ঠা_মান লক্ষ্য = 공간.পৃষ্ঠা_সারণি.get(Integer.valueOf(쪽번호(ইমেইল)));
        if (লক্ষ্য == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return লক্ষ্য;
    }

    private int 쪽번호(int ইমেইল) {
        if (ইমেইল < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ইমেইল / পৃষ্ঠার_মাপ;
    }
}

