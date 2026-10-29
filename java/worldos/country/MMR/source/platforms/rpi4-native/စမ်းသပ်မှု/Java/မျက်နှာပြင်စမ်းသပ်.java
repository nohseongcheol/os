// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class မျက်နှာပြင်စမ်းသပ် {
    public static void main(String[] args) {
        မြန်မာ.ကိုယ်ပိုင်.မျက်နှာပြင်.စတုဂံ(400, 400, 20, 20, 0x123456);
        try { မြန်မာ.ကိုယ်ပိုင်.မျက်နှာပြင်.စတုဂံ(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("မျက်နှာပြင် ဖြတ်နယ်ပယ် တန်ဖိုးငြင်းပယ်"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
