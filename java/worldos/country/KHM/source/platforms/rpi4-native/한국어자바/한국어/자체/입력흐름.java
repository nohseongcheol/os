// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 ស្ទ្រីម_តំលៃ: 순서대로 들어오는 바이트를 읽는 កាណាល់_ការបញ្ចូល. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int អាន() throws ចូល_ចេញ_ការលើកលែង {
        try { return 표준흐름.read();
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public int អាន(byte[] ទិន្នន័យ) throws ចូល_ចេញ_ការលើកលែង {
        try { return 표준흐름.read(ទិន្នន័យ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public int អាន(byte[] ទិន្នន័យ, int រត់, int ប្រវែង_តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try { return 표준흐름.read(ទិន្នន័យ, រត់, ប្រវែង_តំលៃ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public void បិទ() throws ចូល_ចេញ_ការលើកលែង {
        try { 표준흐름.close();
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
}
