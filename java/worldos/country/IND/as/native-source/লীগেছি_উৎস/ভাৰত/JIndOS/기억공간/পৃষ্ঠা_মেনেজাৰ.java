// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB পৃষ্ঠা_মান 연결과 লিখা 시 복사를 제공한다. */
public final class পৃষ্ঠা_মেনেজাৰ {
    public static final int পৃষ্ঠা_আকাৰ = 4096;

    private static final class পৃষ্ঠা_মান {
        private byte[] ডাটা = new byte[পৃষ্ঠা_আকাৰ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ঠিকনা_স্থান {
        private final Map<Integer, পৃষ্ঠা_মান> পৃষ্ঠা_তালিকা = new HashMap<Integer, পৃষ্ঠা_মান>();
    }

    public ঠিকনা_স্থান 새주소공간() {
        return new ঠিকনা_স্থান();
    }

    public void মেপ_পৃষ্ঠা(ঠিকনা_স্থান 공간, int ভাৰ্ছুৱেল_ঠিকনা, boolean 쓰기가능) {
        int ইনডেক্স = 쪽번호(ভাৰ্ছুৱেল_ঠিকনা);
        পৃষ্ঠা_মান 새쪽 = new পৃষ্ঠা_মান();
        새쪽.쓰기가능 = 쓰기가능;
        공간.পৃষ্ঠা_তালিকা.put(Integer.valueOf(ইনডেক্স), 새쪽);
    }

    public ঠিকনা_স্থান 쓰기시복사복제(ঠিকনা_স্থান 원본) {
        ঠিকনা_স্থান 복제본 = new ঠিকনা_স্থান();
        for (Map.Entry<Integer, পৃষ্ঠা_মান> প্রবিষ্ট_মান : 원본.পৃষ্ঠা_তালিকা.entrySet()) {
            পৃষ্ঠা_মান 공유쪽 = প্রবিষ্ট_মান.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.পৃষ্ঠা_তালিকা.put(প্রবিষ্ট_মান.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ঠিকনা_স্থান 공간, int ভাৰ্ছুৱেল_ঠিকনা) {
        পৃষ্ঠা_মান লক্ষ্য = বিচাৰক_পৃষ্ঠা(공간, ভাৰ্ছুৱেল_ঠিকনা);
        return লক্ষ্য.ডাটা[Math.floorMod(ভাৰ্ছুৱেল_ঠিকনা, পৃষ্ঠা_আকাৰ)];
    }

    public void লিখক_বাইট_মান(ঠিকনা_স্থান 공간, int ভাৰ্ছুৱেল_ঠিকনা, byte মান) {
        int ইনডেক্স = 쪽번호(ভাৰ্ছুৱেল_ঠিকনা);
        পৃষ্ঠা_মান লক্ষ্য = বিচাৰক_পৃষ্ঠা(공간, ভাৰ্ছুৱেল_ঠিকনা);
        if (!লক্ষ্য.쓰기가능) {
            if (!লক্ষ্য.쓰기시복사) {
                throw new IllegalStateException("পড়া 전용 쪽입니다.");
            }
            লক্ষ্য = ক্ৰিয়েট_নিজস্ব_পৃষ্ঠা(공간, ইনডেক্স, লক্ষ্য);
        }
        লক্ষ্য.ডাটা[Math.floorMod(ভাৰ্ছুৱেল_ঠিকনা, পৃষ্ঠা_আকাৰ)] = মান;
    }

    public void 범위개인쓰기(ঠিকনা_স্থান 공간, int আৰম্ভ_ঠিকনা, int মাপ) {
        if (মাপ < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int অন্ত_কৰক_ঠিকনা = Math.addExact(আৰম্ভ_ঠিকনা, মাপ);
        for (int ঠিকনা = আৰম্ভ_ঠিকনা; ঠিকনা < অন্ত_কৰক_ঠিকনা; ঠিকনা = (쪽번호(ঠিকনা) + 1) * পৃষ্ঠা_আকাৰ) {
            int ইনডেক্স = 쪽번호(ঠিকনা);
            পৃষ্ঠা_মান লক্ষ্য = বিচাৰক_পৃষ্ঠা(공간, ঠিকনা);
            if (লক্ষ্য.쓰기시복사) {
                ক্ৰিয়েট_নিজস্ব_পৃষ্ঠা(공간, ইনডেক্স, লক্ষ্য);
            } else {
                লক্ষ্য.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ঠিকনা_স্থান 공간, int আৰম্ভ_ঠিকনা, byte[] ডাটা) {
        for (int ইনডেক্স = 0; ইনডেক্স < ডাটা.length; ইনডেক্স++) {
            লিখক_বাইট_মান(공간, আৰম্ভ_ঠিকনা + ইনডেক্স, ডাটা[ইনডেক্স]);
        }
    }

    private পৃষ্ঠা_মান ক্ৰিয়েট_নিজস্ব_পৃষ্ঠা(ঠিকনা_স্থান 공간, int ইনডেক্স, পৃষ্ঠা_মান 공유쪽) {
        পৃষ্ঠা_মান নিজস্ব_পৃষ্ঠা = new পৃষ্ঠা_মান();
        নিজস্ব_পৃষ্ঠা.ডাটা = Arrays.copyOf(공유쪽.ডাটা, 공유쪽.ডাটা.length);
        নিজস্ব_পৃষ্ঠা.쓰기가능 = true;
        নিজস্ব_পৃষ্ঠা.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.পৃষ্ঠা_তালিকা.put(Integer.valueOf(ইনডেক্স), নিজস্ব_পৃষ্ঠা);
        return নিজস্ব_পৃষ্ঠা;
    }

    private পৃষ্ঠা_মান বিচাৰক_পৃষ্ঠা(ঠিকনা_স্থান 공간, int ঠিকনা) {
        পৃষ্ঠা_মান লক্ষ্য = 공간.পৃষ্ঠা_তালিকা.get(Integer.valueOf(쪽번호(ঠিকনা)));
        if (লক্ষ্য == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return লক্ষ্য;
    }

    private int 쪽번호(int ঠিকনা) {
        if (ঠিকনা < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ঠিকনা / পৃষ্ঠা_আকাৰ;
    }
}

