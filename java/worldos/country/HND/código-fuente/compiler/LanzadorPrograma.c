#define _GNU_SOURCE
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void fail(const char *message) {
    fprintf(stderr, "jkoros: %s: %s\n", message, strerror(errno));
    exit(127);
}

int main(int argc, char **argv) {
    char executable[PATH_MAX];
    ssize_t n = readlink("/proc/self/exe", executable, sizeof(executable) - 1);
    if (n < 0 || n == (ssize_t)sizeof(executable) - 1) fail("read executable path");
    executable[n] = '\0';
    const char *parts[] = {@CLASSPATH@};
    char *classpath = calloc(1, 1);
    if (!classpath) fail("allocate classpath");
    for (size_t i = 0; i < sizeof(parts) / sizeof(parts[0]); ++i) {
        char *next = NULL;
        if (asprintf(&next, "%s%s%s.app/%s", classpath, i ? ":" : "", executable, parts[i]) < 0)
            fail("allocate classpath");
        free(classpath);
        classpath = next;
    }
    char *java = NULL;
    if (asprintf(&java, "%s.app/runtime/bin/java", executable) < 0) fail("allocate java path");
    if (access(java, X_OK) != 0) {
        free(java);
        const char *home = getenv("JAVA_HOME");
        if (home && *home) {
            if (asprintf(&java, "%s/bin/java", home) < 0) fail("allocate java path");
        } else {
            java = strdup("java");
            if (!java) fail("allocate java path");
        }
    }
    char **command = calloc((size_t)argc + 4, sizeof(char *));
    if (!command) fail("allocate arguments");
    command[0] = java;
    command[1] = "-cp";
    command[2] = classpath;
    command[3] = @ENTRY@;
    for (int i = 1; i < argc; ++i) command[i + 3] = argv[i];
    execvp(java, command);
    fail("execute OpenJDK (check JAVA_HOME and installed JDK/JRE)");
}
