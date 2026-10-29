// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 출력(出力)과 ნაკადი_მნიშვნელობა: 순서를 보존해 내보내는 바이트의 არხი_შენატანი. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void ჩაწერა(int მნიშვნელობა) throws 입출력예외 {
        try { 표준흐름.write(მნიშვნელობა);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public void ჩაწერა(byte[] მონაცემები) throws 입출력예외 {
        try { 표준흐름.write(მონაცემები);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public void ჩაწერა(byte[] მონაცემები, int გაშვება, int სიგრძე_მნიშვნელობა) throws 입출력예외 {
        try { 표준흐름.write(მონაცემები, გაშვება, სიგრძე_მნიშვნელობა);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public void 내보내기() throws 입출력예외 {
        try { 표준흐름.flush();
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public void დახურვა() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
}
