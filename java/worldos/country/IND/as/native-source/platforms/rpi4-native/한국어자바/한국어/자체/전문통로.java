// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·চেনেল_প্রবিষ্ট(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.খোলো(접속번호);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static 전문통로 খোলো(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public void ই_মেইল_কৰক(String ঠিকনা, int 접속번호, String ডাটা) throws 입출력예외 {
        try { 통신.ই_মেইল_কৰক(표준종단, ঠিকনা, 접속번호, ডাটা);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void বন্ধ_কৰক() { 통신.বন্ধ_কৰক(표준종단); }
}
