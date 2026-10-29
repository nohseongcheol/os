// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gabon.JGabOS.AppelSystème;

public final class détailsSystème {
    private final String nomSystème;
    private final String nomNœud;
    private final String valeurÉdition;
    private final String valeurVersion;
    private final String machine;

    public détailsSystème(String nomSystème, String nomNœud, String valeurÉdition, String valeurVersion, String machine) {
        this.nomSystème = nomSystème;
        this.nomNœud = nomNœud;
        this.valeurÉdition = valeurÉdition;
        this.valeurVersion = valeurVersion;
        this.machine = machine;
    }

    public String nomSystème() { return nomSystème; }
    public String nomNœud() { return nomNœud; }
    public String valeurÉdition() { return valeurÉdition; }
    public String valeurVersion() { return valeurVersion; }
    public String machine() { return machine; }
}
