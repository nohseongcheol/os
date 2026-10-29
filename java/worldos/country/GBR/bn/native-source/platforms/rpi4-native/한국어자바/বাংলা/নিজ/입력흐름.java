// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;

/** 입력(入力)과 প্রবাহ_মান: 순서대로 들어오는 바이트를 읽는 চ্যানেল_ভুক্তি. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int পড়া() throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return 표준흐름.read();
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public int পড়া(byte[] ডাটা) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return 표준흐름.read(ডাটা);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public int পড়া(byte[] ডাটা, int চালনা, int দৈর্ঘ্য_মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return 표준흐름.read(ডাটা, চালনা, দৈর্ঘ্য_মান);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public void বন্ধ_করুন() throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준흐름.close();
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
}
