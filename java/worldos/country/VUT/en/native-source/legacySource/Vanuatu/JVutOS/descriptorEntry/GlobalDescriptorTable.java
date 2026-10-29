// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Vanuatu.JVutOS.descriptorEntry;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Stores x86 global descriptor table and task-state segment settings. */
public final class GlobalDescriptorTable {
    public static final class fragmentValue {
        private final int backgroundValue;
        private final int boundaryLimit;
        private final int accessValue;

        fragmentValue(int backgroundValue, int boundaryLimit, int accessValue) {
            this.backgroundValue = backgroundValue;
            this.boundaryLimit = boundaryLimit;
            this.accessValue = accessValue;
        }

        public int backgroundValue() { return backgroundValue; }
        public int boundaryLimit() { return boundaryLimit; }
        public int accessValue() { return accessValue; }
    }

    private final List<fragmentValue> fragmentsList = new ArrayList<fragmentValue>();

    public int appendEntry(int backgroundValue, int boundaryLimit, int accessValue) {
        fragmentsList.add(new fragmentValue(backgroundValue, boundaryLimit, accessValue));
        return (fragmentsList.size() - 1) * 8;
    }

    public List<fragmentValue> fragmentsList() {
        return Collections.unmodifiableList(fragmentsList);
    }

    public void setDefaultValue() {
        fragmentsList.clear();
        appendEntry(0, 0, 0);
        appendEntry(0, 0xfffff, 0x9a);
        appendEntry(0, 0xfffff, 0x92);
        appendEntry(0, 0xfffff, 0xfa);
        appendEntry(0, 0xfffff, 0xf2);
    }
}

