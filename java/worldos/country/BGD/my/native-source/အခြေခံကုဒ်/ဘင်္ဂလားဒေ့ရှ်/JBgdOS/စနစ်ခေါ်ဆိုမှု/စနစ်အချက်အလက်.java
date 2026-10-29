// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ဘင်္ဂလားဒေ့ရှ်.JBgdOS.စနစ်ခေါ်ဆိုမှု;

public final class စနစ်အချက်အလက် {
    private final String စနစ်အမည်;
    private final String ဆုံမှတ်အမည်;
    private final String ဘာသာစကားထုတ်ဝေမှုတန်ဖိုး;
    private final String ထုတ်ဝေမှုတန်ဖိုး;
    private final String စက်;

    public စနစ်အချက်အလက်(String စနစ်အမည်, String ဆုံမှတ်အမည်, String ဘာသာစကားထုတ်ဝေမှုတန်ဖိုး, String ထုတ်ဝေမှုတန်ဖိုး, String စက်) {
        this.စနစ်အမည် = စနစ်အမည်;
        this.ဆုံမှတ်အမည် = ဆုံမှတ်အမည်;
        this.ဘာသာစကားထုတ်ဝေမှုတန်ဖိုး = ဘာသာစကားထုတ်ဝေမှုတန်ဖိုး;
        this.ထုတ်ဝေမှုတန်ဖိုး = ထုတ်ဝေမှုတန်ဖိုး;
        this.စက် = စက်;
    }

    public String စနစ်အမည်() { return စနစ်အမည်; }
    public String ဆုံမှတ်အမည်() { return ဆုံမှတ်အမည်; }
    public String ဘာသာစကားထုတ်ဝေမှုတန်ဖိုး() { return ဘာသာစကားထုတ်ဝေမှုတန်ဖိုး; }
    public String ထုတ်ဝေမှုတန်ဖိုး() { return ထုတ်ဝေမှုတန်ဖိုး; }
    public String စက်() { return စက်; }
}
