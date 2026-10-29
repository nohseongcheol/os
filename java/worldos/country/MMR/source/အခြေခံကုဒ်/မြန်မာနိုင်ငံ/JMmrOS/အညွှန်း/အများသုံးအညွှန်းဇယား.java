// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာနိုင်ငံ.JMmrOS.အညွှန်း;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 အများသုံးအညွှန်းဇယားနှင့် အလုပ်အခြေအနေအပိုင်း သတ်မှတ်ချက်များကို သိမ်းသည်။ */
public final class အများသုံးအညွှန်းဇယား {
    public static final class အစိတ်အပိုင်း {
        private final int နောက်ခံတန်ဖိုး;
        private final int နယ်နိမိတ်ကန့်သတ်ချက်;
        private final int ဝင်သုံးတန်ဖိုး;

        အစိတ်အပိုင်း(int နောက်ခံတန်ဖိုး, int နယ်နိမိတ်ကန့်သတ်ချက်, int ဝင်သုံးတန်ဖိုး) {
            this.နောက်ခံတန်ဖိုး = နောက်ခံတန်ဖိုး;
            this.နယ်နိမိတ်ကန့်သတ်ချက် = နယ်နိမိတ်ကန့်သတ်ချက်;
            this.ဝင်သုံးတန်ဖိုး = ဝင်သုံးတန်ဖိုး;
        }

        public int နောက်ခံတန်ဖိုး() { return နောက်ခံတန်ဖိုး; }
        public int နယ်နိမိတ်ကန့်သတ်ချက်() { return နယ်နိမိတ်ကန့်သတ်ချက်; }
        public int ဝင်သုံးတန်ဖိုး() { return ဝင်သုံးတန်ဖိုး; }
    }

    private final List<အစိတ်အပိုင်း> အပိုင်းအစများ = new ArrayList<အစိတ်အပိုင်း>();

    public int အချက်နောက်တွဲ(int နောက်ခံတန်ဖိုး, int နယ်နိမိတ်ကန့်သတ်ချက်, int ဝင်သုံးတန်ဖိုး) {
        အပိုင်းအစများ.add(new အစိတ်အပိုင်း(နောက်ခံတန်ဖိုး, နယ်နိမိတ်ကန့်သတ်ချက်, ဝင်သုံးတန်ဖိုး));
        return (အပိုင်းအစများ.size() - 1) * 8;
    }

    public List<အစိတ်အပိုင်း> အပိုင်းအစများ() {
        return Collections.unmodifiableList(အပိုင်းအစများ);
    }

    public void မူလသတ်မှတ်တန်ဖိုးသတ်မှတ်() {
        အပိုင်းအစများ.clear();
        အချက်နောက်တွဲ(0, 0, 0);
        အချက်နောက်တွဲ(0, 0xfffff, 0x9a);
        အချက်နောက်တွဲ(0, 0xfffff, 0x92);
        အချက်နောက်တွဲ(0, 0xfffff, 0xfa);
        အချက်နောက်တွဲ(0, 0xfffff, 0xf2);
    }
}

