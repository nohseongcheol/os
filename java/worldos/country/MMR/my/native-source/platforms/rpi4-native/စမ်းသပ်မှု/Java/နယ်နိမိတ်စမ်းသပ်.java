// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class နယ်နိမိတ်စမ်းသပ် {
    static int မအောင်မြင်မှု() { throw new IllegalStateException("အလုပ် 중 ခြွင်းချက်"); }
    public static void main(String[] a) throws Exception {
        Object ရိုးရိုးအခင်း = new Object[2]; System.out.println(ရိုးရိုးအခင်း instanceof String[]);
        try { String[] မမှန်ကန်ရလဒ် = (String[])ရိုးရိုးအခင်း; } catch (ClassCastException e) { System.out.println("အခင်းအကျင်းတန်ဖိုး တန်ဖိုးပြောင်းလဲ စစ်ဆေးချက်"); }
        Object[] စာသားများ = new String[2];
        try { စာသားများ[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("အခင်းအကျင်းတန်ဖိုး အမျိုးပုံစံတန်ဖိုး စစ်ဆေးချက်"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, စာသားများ, 0, 2); } catch (ArrayStoreException e) { System.out.println("တန်ဖိုးမိတ္တူကူး အမျိုးပုံစံတန်ဖိုး စစ်ဆေးချက်"); }
        System.out.println((String)စာသားများ[0]);
        try { "글".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("အက္ခရာ ဖြတ်နယ်ပယ်"); }
        Integer တစ်တန်ဖိုး = Integer.valueOf(127), နှစ်တန်ဖိုး = Integer.valueOf(127); System.out.println(တစ်တန်ဖိုး == နှစ်တန်ဖိုး);
        Object သော့ခတ်တန်ဖိုး = new Object(); try { synchronized (သော့ခတ်တန်ဖိုး) { မအောင်မြင်မှု(); } } catch (IllegalStateException e) { System.out.println("သော့ခတ်တန်ဖိုး ခြွင်းချက်"); }
        synchronized (သော့ခတ်တန်ဖိုး) { System.out.println("သော့ခတ်တန်ဖိုး 회수"); }
        byte[] ဒေတာ = {0, (byte)128, (byte)255, 10};
        FileOutputStream အထွက် = new FileOutputStream("ဘိုက်တန်ဖိုး.bin"); အထွက်.write(ဒေတာ); အထွက်.flush(); အထွက်.close();
        FileInputStream ဝင်ဒေတာ = new FileInputStream("ဘိုက်တန်ဖိုး.bin"); byte[] ရလဒ်ဖတ် = new byte[8];
        System.out.println(ဝင်ဒေတာ.read(ရလဒ်ဖတ်, 2, 4)); System.out.println(ရလဒ်ဖတ်[3] + ":" + ရလဒ်ဖတ်[4]);
        System.out.println(ဝင်ဒေတာ.read(ရလဒ်ဖတ်)); System.out.println(ဝင်ဒေတာ.read(ရလဒ်ဖတ်, 0, 0)); ဝင်ဒေတာ.close();
        try { ဝင်ဒေတာ.read(); } catch (IOException e) { System.out.println("닫힌 ဖိုင်"); }
    }
}
