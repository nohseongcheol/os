// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ব্যৱহাৰকৰ্তা 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class নথিপত্ৰ {
    private নথিপত্ৰ() {}
    public static byte[] 바이트읽기(String নাম) throws 입출력예외 {
        try {
        FileInputStream ষ্ট্ৰিম_মান = new FileInputStream(নাম);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, মান;
            while ((মান = ষ্ট্ৰিম_মান.read()) != -1) { if (수 == 임시.length) throw new 입출력예외("নথিপত্ৰ মাপ 제한"); 임시[수++] = (byte)মান; }
            byte[] পৰিমাপ = new byte[수]; System.arraycopy(임시, 0, পৰিমাপ, 0, 수); return পৰিমাপ;
        } finally { ষ্ট্ৰিম_মান.close(); }
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static void লিখক_বাইট_মান(String নাম, byte[] সামগ্ৰী_মান) throws 입출력예외 {
        try {
        FileOutputStream ষ্ট্ৰিম_মান = new FileOutputStream(নাম);
        try { for (int লুপ_ইনডেক্স = 0; লুপ_ইনডেক্স < সামগ্ৰী_মান.length; লুপ_ইনডেক্স++) ষ্ট্ৰিম_মান.write(সামগ্ৰী_মান[লুপ_ইনডেক্স] & 255); } finally { ষ্ট্ৰিম_মান.close(); }
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static String পড়া(String নাম) throws 입출력예외 {
        try { return 문자.ডিক্ৰিপ্ট_কৰক_ডাটা(바이트읽기(নাম));
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static void লিখা(String নাম, String সামগ্ৰী_মান) throws 입출력예외 {
        try { লিখক_বাইট_মান(নাম, 문자.부호화(সামগ্ৰী_মান));
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
}
