// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 ნაკადი_მნიშვნელობა: 순서대로 들어오는 바이트를 읽는 არხი_შენატანი. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int კითხვა() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public int კითხვა(byte[] მონაცემები) throws 입출력예외 {
        try { return 표준흐름.read(მონაცემები);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public int კითხვა(byte[] მონაცემები, int გაშვება, int სიგრძე_მნიშვნელობა) throws 입출력예외 {
        try { return 표준흐름.read(მონაცემები, გაშვება, სიგრძე_მნიშვნელობა);
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
    public void დახურვა() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException შეცდომა) { throw 예외변환.შეტანა_გამოტანა(შეცდომა); }
        catch (RuntimeException შეცდომა) { throw 예외변환.შესრულება_ბრძანება(შეცდომა); }
    }
}
