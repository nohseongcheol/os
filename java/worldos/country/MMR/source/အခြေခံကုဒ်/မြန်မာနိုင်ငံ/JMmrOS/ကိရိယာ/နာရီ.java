// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package မြန်မာနိုင်ငံ.JMmrOS.ကိရိယာ;

/** PIT အလွှာမှ တင်သော စည်းချက်များနှင့် အလှည့်ဖြတ်ချိန်ကို စီမံသည်။ */
public final class နာရီ {
    private final int တစ်စက္ကန့်စည်းချက်;
    private long နာရီချက်အရေအတွက်;

    public နာရီ(int တစ်စက္ကန့်စည်းချက်) {
        if (တစ်စက္ကန့်စည်းချက် <= 0) {
            throw new IllegalArgumentException("초당 နာရီချက်တန်ဖိုး 수가 올바르지 않습니다.");
        }
        this.တစ်စက္ကန့်စည်းချက် = တစ်စက္ကန့်စည်းချက်;
    }

    public long နာရီချက်တန်ဖိုး() {
        return ++နာရီချက်အရေအတွက်;
    }

    public long နာရီချက်အရေအတွက်() {
        return နာရီချက်အရေအတွက်;
    }

    public long ကုန်လွန်မီလီစက္ကန့်() {
        return နာရီချက်အရေအတွက် * 1000L / တစ်စက္ကန့်စည်းချက်;
    }
}

