// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ব্যবহারকারী 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class নথির_নাম {
    private নথির_নাম() {}
    public static byte[] 바이트읽기(String নাম) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try {
        FileInputStream প্রবাহ_মান = new FileInputStream(নাম);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, মান;
            while ((মান = প্রবাহ_মান.read()) != -1) { if (수 == 임시.length) throw new ইনপুট_আউটপুট_ব্যতিক্রম("নথির_নাম আকার 제한"); 임시[수++] = (byte)মান; }
            byte[] পরিমাপ = new byte[수]; System.arraycopy(임시, 0, পরিমাপ, 0, 수); return পরিমাপ;
        } finally { প্রবাহ_মান.close(); }
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static void লেখা_বাইট_মান(String নাম, byte[] সামগ্রি_মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try {
        FileOutputStream প্রবাহ_মান = new FileOutputStream(নাম);
        try { for (int লুপ_সূচি = 0; লুপ_সূচি < সামগ্রি_মান.length; লুপ_সূচি++) প্রবাহ_মান.write(সামগ্রি_মান[লুপ_সূচি] & 255); } finally { প্রবাহ_মান.close(); }
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static String পড়া(String নাম) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return 문자.ডিক্রিপ্ট_ডাটা(바이트읽기(নাম));
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static void লেখা(String নাম, String সামগ্রি_মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { লেখা_বাইট_মান(নাম, 문자.부호화(সামগ্রি_মান));
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
}
