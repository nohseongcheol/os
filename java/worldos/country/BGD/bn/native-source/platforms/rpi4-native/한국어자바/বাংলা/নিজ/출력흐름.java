// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;

/** নির্গম(出力)과 প্রবাহ_মান: 순서를 보존해 내보내는 바이트의 চ্যানেল_ভুক্তি. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void লেখা(int মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준흐름.write(মান);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public void লেখা(byte[] ডাটা) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준흐름.write(ডাটা);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public void লেখা(byte[] ডাটা, int চালনা, int দৈর্ঘ্য_মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준흐름.write(ডাটা, চালনা, দৈর্ঘ্য_মান);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public void 내보내기() throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준흐름.flush();
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public void বন্ধ_করুন() throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준흐름.close();
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
}
