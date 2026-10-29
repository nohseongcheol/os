// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PC/AT PS/2 ပြောင်းလဲအစု 1 ကို လှည့်စစ်ဖတ်သည်။ အခြေခံ အမေရိကန်လက်ကွက်၊ Shift၊ Backspace နှင့် Enter ကို ပံ့ပိုးသည်။ */
public final class လက်ကွက် {
    static boolean ရွှေ့ပြောင်းဘယ် = false;
    static boolean ရွှေ့ပြောင်းညာ = false;
    static boolean တိုးချဲ့မှု = false;
    static String မူလသတ်မှတ်တန်ဖိုး = "\0\0" + "1234567890-=\b\tqwertyuiop[]\n\0asdfghjkl;'`\0\\zxcvbnm,./\0*\0 ";
    static String ရွှေ့ပြောင်းတန်ဖိုး = "\0\0" + "!@#$%^&*()_+\b\tQWERTYUIOP{}\n\0ASDFGHJKL:\"~\0|ZXCVBNM<>?\0*\0 ";

    static int ဖတ်() {
        int အခြေအနေတန်ဖိုး = ကိရိယာ.အဝင်အထွက်ဘိုက်ဖတ်(0x64);
        if ((အခြေအနေတန်ဖိုး & 1) == 0) return -1;
        int တန်ဖိုး = ကိရိယာ.အဝင်အထွက်ဘိုက်ဖတ်(0x60);
        if ((အခြေအနေတန်ဖိုး & 0x20) != 0) return -1;
        if (တန်ဖိုး == 0xe0 || တန်ဖိုး == 0xe1) { တိုးချဲ့မှု = true; return -1; }
        if (တိုးချဲ့မှု) { တိုးချဲ့မှု = false; return -1; }
        if (တန်ဖိုး == 42 || တန်ဖိုး == 170) { ရွှေ့ပြောင်းဘယ် = တန်ဖိုး == 42; return -1; }
        if (တန်ဖိုး == 54 || တန်ဖိုး == 182) { ရွှေ့ပြောင်းညာ = တန်ဖိုး == 54; return -1; }
        if (တန်ဖိုး >= မူလသတ်မှတ်တန်ဖိုး.length()) return -1;
        int အက္ခရာ = (ရွှေ့ပြောင်းဘယ် || ရွှေ့ပြောင်းညာ) ? ရွှေ့ပြောင်းတန်ဖိုး.charAt(တန်ဖိုး) : မူလသတ်မှတ်တန်ဖိုး.charAt(တန်ဖိုး);
        return အက္ခရာ == 0 ? -1 : အက္ခရာ;
    }
}
