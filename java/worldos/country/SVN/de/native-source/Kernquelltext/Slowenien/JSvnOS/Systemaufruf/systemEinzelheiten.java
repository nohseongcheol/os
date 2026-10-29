// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slowenien.JSvnOS.Systemaufruf;

public final class systemEinzelheiten {
    private final String systemName;
    private final String knotenName;
    private final String ausgabeversionWert;
    private final String versionWert;
    private final String maschine;

    public systemEinzelheiten(String systemName, String knotenName, String ausgabeversionWert, String versionWert, String maschine) {
        this.systemName = systemName;
        this.knotenName = knotenName;
        this.ausgabeversionWert = ausgabeversionWert;
        this.versionWert = versionWert;
        this.maschine = maschine;
    }

    public String systemName() { return systemName; }
    public String knotenName() { return knotenName; }
    public String ausgabeversionWert() { return ausgabeversionWert; }
    public String versionWert() { return versionWert; }
    public String maschine() { return maschine; }
}
