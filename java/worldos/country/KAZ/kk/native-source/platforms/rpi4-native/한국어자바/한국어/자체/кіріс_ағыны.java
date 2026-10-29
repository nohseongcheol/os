// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 ағым_мән: 순서대로 들어오는 바이트를 읽는 Арна_енгізу. */
public final class кіріс_ағыны {
    private final java.io.InputStream 표준흐름;
    кіріс_ағыны(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Оқу() throws енгізу_шығару_ерекшелік {
        try { return 표준흐름.read();
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public int Оқу(byte[] деректер) throws енгізу_шығару_ерекшелік {
        try { return 표준흐름.read(деректер);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public int Оқу(byte[] деректер, int Орындау_2, int ұзындық_мән) throws енгізу_шығару_ерекшелік {
        try { return 표준흐름.read(деректер, Орындау_2, ұзындық_мән);
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
    public void Жабу() throws енгізу_шығару_ерекшелік {
        try { 표준흐름.close();
        } catch (java.io.IOException Қате) { throw Түрлендіру_ерекшелік.енгізу_шығару(Қате); }
        catch (RuntimeException Қате) { throw Түрлендіру_ерекшелік.орындау_пәрмен(Қате); }
    }
}
