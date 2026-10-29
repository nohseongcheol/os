// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package United_Kingdom.JGbrOS.FileSystem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** Managed model of read-only file storage corresponding to the engos FAT reading layer. */
public final class FileSystem {
    static final class openedFile {
        final byte[] data;
        int position;
        int referenceCount = 1;

        openedFile(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> fileEntries = new LinkedHashMap<String, byte[]>();

    public void appendFile(String name, byte[] data) {
        fileEntries.put(canonicalName(name), Arrays.copyOf(data, data.length));
    }

    openedFile open(String name) {
        byte[] data = fileEntries.get(canonicalName(name));
        if (data == null) {
            return null;
        }
        return new openedFile(data);
    }

    public boolean existsValue(String name) {
        return fileEntries.containsKey(canonicalName(name));
    }

    public fileInformation systemInformation(String name) {
        byte[] data = fileEntries.get(canonicalName(name));
        if (data == null) {
            return null;
        }
        return new fileInformation(data.length, 0100444);
    }

    private String canonicalName(String name) {
        if (name == null) {
            throw new NullPointerException("file 이름이 없습니다.");
        }
        String result = name.startsWith("/") ? name.substring(1) : name;
        return result.toUpperCase(Locale.ROOT);
    }
}
