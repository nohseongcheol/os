/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"sync"
)

type result struct {
	code  string
	error error
}

func managementPath(root, relative string) string {
	data, err := ioutil.ReadFile(filepath.Join(root, "layout.json"))
	if os.IsNotExist(err) {
		return filepath.Join(root, relative)
	}
	var layout struct {
		Version int               `json:"version"`
		Paths   map[string]string `json:"paths"`
	}
	if err != nil || json.Unmarshal(data, &layout) != nil || layout.Version != 1 {
		panic("invalid management layout: " + root)
	}
	if name, ok := layout.Paths[relative]; ok {
		relative = name
	}
	if filepath.IsAbs(relative) || relative == ".." || strings.HasPrefix(filepath.Clean(relative), "../") {
		panic("unsafe management path: " + relative)
	}
	return filepath.Join(root, relative)
}

func allowedASCIISequence(word string, allowed map[string]bool) bool {
	if allowed[word] {
		return true
	}
	reachable := make([]bool, len(word)+1)
	reachable[0] = true
	for end := 1; end <= len(word); end++ {
		for start := 0; start < end; start++ {
			if reachable[start] && allowed[word[start:end]] {
				reachable[end] = true
				break
			}
		}
	}
	return reachable[len(word)]
}

func verifyTree(path string) error {
	mapped, err := sourcePaths(path)
	if err != nil {
		return err
	}
	resolve := func(relative string) string {
		if value := mapped[relative]; value != "" {
			return value
		}
		return relative
	}
	for _, required := range []string{"Makefile", "go.sh", "linker.ld", "README.md", "나라언어.md", "이름대응표.tsv", "파일대응표.tsv", "용어사전.tsv", "용어근거.tsv", "src", "asm", "tools/decode-virtualbox-log.sh", "userland/posix/Makefile", "userland/posix/linker.ld", "userland/posix/include/unistd.h", "userland/posix/src/unistd.c"} {
		if required == "asm" {
			required = filepath.Dir(resolve("asm/rt0.s"))
		}
		if _, err := os.Stat(filepath.Join(path, resolve(required))); err != nil {
			return fmt.Errorf("missing %s", required)
		}
	}
	goFiles := 1  // main.go
	asmFiles := 1 // main.s
	err = filepath.Walk(filepath.Join(path, "src"), func(current string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			switch filepath.Ext(info.Name()) {
			case ".go":
				goFiles++
			case ".s":
				asmFiles++
			}
		}
		return nil
	})
	if err != nil {
		return err
	}
	assemblyEntries, err := ioutil.ReadDir(filepath.Join(path, filepath.Dir(resolve("asm/rt0.s"))))
	if err != nil {
		return err
	}
	for _, entry := range assemblyEntries {
		if !entry.IsDir() && filepath.Ext(entry.Name()) == ".s" {
			asmFiles++
		}
	}
	if goFiles != 43 || asmFiles != 14 {
		return fmt.Errorf("source count mismatch: go=%d asm=%d", goFiles, asmFiles)
	}
	details, err := ioutil.ReadFile(managementPath(path, "나라언어.md"))
	if err != nil {
		return err
	}
	language := ""
	for _, line := range strings.Split(string(details), "\n") {
		if strings.HasPrefix(line, "- selected language: ") {
			language = strings.TrimPrefix(line, "- selected language: ")
			break
		}
	}
	baseLanguage := strings.SplitN(language, "_", 2)[0]
	nonLatinNative := map[string]bool{"am": true, "ar": true, "be": true, "bg": true, "el": true, "fa": true, "he": true, "hy": true, "ja": true, "ka": true, "ko": true, "ky": true, "mk": true, "mn": true, "ru": true, "sr": true, "tg": true, "ti": true, "uk": true, "ur": true, "zh": true}
	if nonLatinNative[baseLanguage] && !strings.Contains(language, "Latn") {
		allowed := map[string]bool{"go": true, "s": true, "amd": true, "am": true, "amdam": true, "gateamd": true, "ata": true, "arp": true, "icmp": true, "ipv": true, "udp": true, "tcp": true, "pci": true, "gdt": true, "tss": true, "elf": true, "fat": true, "msdos": true, "vga": true, "cpu": true, "cr": true, "c": true, "ethernet": true}
		// A source-glossary fallback may remain visibly English, but it must
		// stay documented as unresolved. It must never be disguised by an
		// invented letter-by-letter reading in the target script.
		evidence, evidenceErr := ioutil.ReadFile(managementPath(path, "용어근거.tsv"))
		if evidenceErr != nil {
			return evidenceErr
		}
		for index, line := range strings.Split(string(evidence), "\n") {
			if index == 0 || line == "" {
				continue
			}
			fields := strings.Split(line, "\t")
			if len(fields) >= 3 && fields[2] == "fallback-English" {
				allowed[strings.ToLower(fields[0])] = true
			}
		}
		asciiWord := regexp.MustCompile(`[A-Za-z]+`)
		// Reviewed project phrases and explicitly pending English fallbacks are
		// declared in the new full-concept ledger, never disguised as native text.
		if phrases, readErr := ioutil.ReadFile(managementPath(path, "새명명-용어.tsv")); readErr == nil {
			for index, line := range strings.Split(string(phrases), "\n") {
				fields := strings.Split(line, "\t")
				if index > 0 && len(fields) >= 4 {
					for _, word := range asciiWord.FindAllString(strings.ToLower(fields[2]), -1) {
						allowed[word] = true
					}
				}
			}
		}
		err := filepath.Walk(filepath.Join(path, "src"), func(current string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			relative, _ := filepath.Rel(filepath.Join(path, "src"), current)
			for _, word := range asciiWord.FindAllString(strings.ToLower(relative), -1) {
				if !allowedASCIISequence(word, allowed) {
					return fmt.Errorf("undocumented English source-path word %q for %s: %s", word, language, relative)
				}
			}
			return nil
		})
		if err != nil {
			return err
		}
	}
	for _, root := range []string{path, filepath.Dir(path)} {
		err := filepath.Walk(root, func(current string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if info.IsDir() && (info.Name() == "build" || current != root && root == filepath.Dir(path) && current == path) {
				return filepath.SkipDir
			}
			if info.Mode()&os.ModeSymlink != 0 {
				return fmt.Errorf("symbolic link is not independent: %s", current)
			}
			return nil
		})
		if err != nil {
			return err
		}
	}
	for _, relative := range []string{"이름대응표.tsv", "파일대응표.tsv"} {
		data, err := ioutil.ReadFile(managementPath(path, relative))
		if err != nil {
			return err
		}
		if regexp.MustCompile(`(?m)[[:alpha:]]+_[0-9a-f]{8}([.\t/]|$)`).Match(data) {
			return fmt.Errorf("legacy language-token/hash name remains in %s", relative)
		}
	}
	for _, relative := range []string{"Makefile", "go.sh"} {
		data, err := ioutil.ReadFile(filepath.Join(path, resolve(relative)))
		if err != nil {
			return err
		}
		text := string(data)
		if strings.Contains(text, "/home/user/engos") || strings.Contains(text, "/home/user/worldos") || strings.Contains(text, "/home/user/test1") || strings.Contains(text, "../../공통") {
			return fmt.Errorf("external project dependency remains in %s", relative)
		}
	}
	countryMakefile, err := ioutil.ReadFile(filepath.Join(filepath.Dir(path), "Makefile"))
	if err != nil {
		return err
	}
	if strings.Contains(string(countryMakefile), "../../공통") || strings.Contains(string(countryMakefile), "/home/user/") {
		return fmt.Errorf("country Makefile is not independent")
	}
	userlandMakefile, err := ioutil.ReadFile(filepath.Join(path, resolve("userland/posix/Makefile")))
	if err != nil {
		return err
	}
	if strings.Contains(string(userlandMakefile), "../user/") || strings.Contains(string(userlandMakefile), "/home/user/") {
		return fmt.Errorf("POSIX userland has an external linker-script dependency")
	}
	return nil
}

func sourcePaths(path string) (map[string]string, error) {
	data, err := ioutil.ReadFile(managementPath(path, "파일대응표.tsv"))
	if err != nil {
		return nil, err
	}
	mapped := map[string]string{}
	for _, name := range []string{"나라언어.md", "이름대응표.tsv", "파일대응표.tsv", "용어사전.tsv", "용어근거.tsv"} {
		mapped[name], err = filepath.Rel(path, managementPath(path, name))
		if err != nil {
			return nil, err
		}
	}
	for index, line := range strings.Split(string(data), "\n") {
		fields := strings.Split(line, "\t")
		if index == 0 || len(fields) != 2 {
			continue
		}
		if filepath.IsAbs(fields[1]) || strings.Contains(fields[1], "../") {
			return nil, fmt.Errorf("unsafe mapped path: %s", fields[1])
		}
		if _, err := os.Stat(filepath.Join(path, fields[1])); err != nil {
			return nil, err
		}
		mapped[fields[0]] = fields[1]
	}
	return mapped, nil
}

func build(root, code, logRoot string) error {
	// Force recompilation: the legacy Makefile has no Go source prerequisites.
	command := exec.Command("make", "-B", "-C", filepath.Join(root, "나라", code), "source")
	output, err := command.CombinedOutput()
	if err == nil {
		path := managementPath(filepath.Join(root, "나라", code), "소스")
		mapped, mapErr := sourcePaths(path)
		if mapErr != nil {
			return mapErr
		}
		makefile := mapped["userland/posix/Makefile"]
		if makefile == "" {
			makefile = "userland/posix/Makefile"
		}
		userland := exec.Command("make", "-B", "-C", filepath.Join(path, filepath.Dir(makefile)), "check", "test-programs")
		userOutput, userErr := userland.CombinedOutput()
		output = append(output, userOutput...)
		err = userErr
	}
	if writeError := ioutil.WriteFile(filepath.Join(logRoot, code+".log"), output, 0644); writeError != nil {
		return writeError
	}
	if err != nil {
		return err
	}
	if _, err := os.Stat(filepath.Join(managementPath(filepath.Join(root, "나라", code), "소스"), "build", "kernel.bin")); err != nil {
		return fmt.Errorf("kernel.bin missing after successful make")
	}
	return nil
}

func main() {
	rootFlag := flag.String("root", "/home/user/worldos", "WorldOS root")
	buildFlag := flag.Bool("build", false, "build every independent kernel")
	workersFlag := flag.Int("workers", 4, "parallel build workers")
	flag.Parse()

	entries, err := ioutil.ReadDir(filepath.Join(*rootFlag, "나라"))
	if err != nil {
		panic(err)
	}
	var codes []string
	for _, entry := range entries {
		if entry.IsDir() && len(entry.Name()) == 3 {
			codes = append(codes, entry.Name())
		}
	}
	sort.Strings(codes)
	if len(codes) != 249 {
		panic(fmt.Sprintf("expected 249 country directories, got %d", len(codes)))
	}
	for _, code := range codes {
		if err := verifyTree(managementPath(filepath.Join(*rootFlag, "나라", code), "소스")); err != nil {
			panic(fmt.Sprintf("%s: %v", code, err))
		}
	}
	if !*buildFlag {
		fmt.Printf("country source structure OK: %d/249\n", len(codes))
		return
	}

	logRoot := filepath.Join(*rootFlag, "build-verification")
	if err := os.MkdirAll(logRoot, 0755); err != nil {
		panic(err)
	}
	jobs := make(chan string)
	results := make(chan result)
	var workers sync.WaitGroup
	for i := 0; i < *workersFlag; i++ {
		workers.Add(1)
		go func() {
			defer workers.Done()
			for code := range jobs {
				results <- result{code: code, error: build(*rootFlag, code, logRoot)}
			}
		}()
	}
	go func() {
		workers.Wait()
		close(results)
	}()
	go func() {
		for _, code := range codes {
			jobs <- code
		}
		close(jobs)
	}()

	completed := 0
	var failures []string
	for item := range results {
		completed++
		if item.error != nil {
			failures = append(failures, item.code+":"+item.error.Error())
		}
		if completed%10 == 0 || completed == len(codes) {
			fmt.Printf("verified country builds: %d/%d failures=%d\n", completed, len(codes), len(failures))
		}
	}
	status := "country\tstatus\n"
	failed := map[string]string{}
	for _, failure := range failures {
		parts := strings.SplitN(failure, ":", 2)
		failed[parts[0]] = parts[1]
	}
	for _, code := range codes {
		if message := failed[code]; message != "" {
			status += code + "\tFAIL " + message + "\n"
		} else {
			status += code + "\tPASS\n"
		}
	}
	if err := ioutil.WriteFile(filepath.Join(logRoot, "status.tsv"), []byte(status), 0644); err != nil {
		panic(err)
	}
	if len(failures) != 0 {
		panic(fmt.Sprintf("%d country builds failed: %s", len(failures), strings.Join(failures, ", ")))
	}
	fmt.Printf("all independent country kernels built successfully: %d/249\n", len(codes))
}
