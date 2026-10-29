// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** លទ្ធផល(出力)과 ស្ទ្រីម_តំលៃ: 순서를 보존해 내보내는 바이트의 កាណាល់_ការបញ្ចូល. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void សរសេរ(int តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try { 표준흐름.write(តំលៃ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public void សរសេរ(byte[] ទិន្នន័យ) throws ចូល_ចេញ_ការលើកលែង {
        try { 표준흐름.write(ទិន្នន័យ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public void សរសេរ(byte[] ទិន្នន័យ, int រត់, int ប្រវែង_តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try { 표준흐름.write(ទិន្នន័យ, រត់, ប្រវែង_តំលៃ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public void 내보내기() throws ចូល_ចេញ_ការលើកលែង {
        try { 표준흐름.flush();
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public void បិទ() throws ចូល_ចេញ_ការលើកលែង {
        try { 표준흐름.close();
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
}
