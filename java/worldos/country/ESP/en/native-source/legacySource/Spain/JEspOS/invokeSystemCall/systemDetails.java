// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Spain.JEspOS.invokeSystemCall;

public final class systemDetails {
    private final String systemName;
    private final String nodeName;
    private final String editionValue;
    private final String versionValue;
    private final String machine;

    public systemDetails(String systemName, String nodeName, String editionValue, String versionValue, String machine) {
        this.systemName = systemName;
        this.nodeName = nodeName;
        this.editionValue = editionValue;
        this.versionValue = versionValue;
        this.machine = machine;
    }

    public String systemName() { return systemName; }
    public String nodeName() { return nodeName; }
    public String editionValue() { return editionValue; }
    public String versionValue() { return versionValue; }
    public String machine() { return machine; }
}
