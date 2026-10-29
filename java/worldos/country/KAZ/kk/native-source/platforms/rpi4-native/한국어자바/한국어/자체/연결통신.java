// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static қосылым Ашу(String мекенжай, int порт_нөмірі) throws енгізу_шығару_ерекшелік {
        try { return қосылым.Ашу(мекенжай, порт_нөмірі);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static 수신창구 수신열기(int порт_нөмірі) throws енгізу_шығару_ерекшелік {
        try { return 수신창구.Ашу(порт_нөмірі);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static Socket Байланысу(String мекенжай, int порт_мән) throws енгізу_шығару_ерекшелік {
        try { return new Socket(мекенжай, порт_мән);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static ServerSocket деректердің_берілуін_күту_қатысушы(int порт_мән) throws енгізу_шығару_ерекшелік {
        try { return new ServerSocket(порт_мән);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public static Socket 받기(ServerSocket сервер_мән) throws енгізу_шығару_ерекшелік {
        try { return сервер_мән.accept();
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
}
