/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
)

func verify(root, kind, config string) (int, error) {
	entries, err := ioutil.ReadDir(filepath.Join(root, kind))
	if err != nil {
		return 0, err
	}
	count := 0
	for _, entry := range entries {
		if !entry.IsDir() {
			continue
		}
		if len(entry.Name()) != 3 {
			return count, fmt.Errorf("invalid code directory: %s/%s", kind, entry.Name())
		}
		for _, required := range []string{"Makefile", config} {
			if _, err := os.Stat(filepath.Join(root, kind, entry.Name(), required)); err != nil {
				return count, fmt.Errorf("%s/%s: missing %s", kind, entry.Name(), required)
			}
		}
		count++
	}
	return count, nil
}

func indexLines(path string) (int, error) {
	f, err := os.Open(path)
	if err != nil {
		return 0, err
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)
	count := -1 // header
	for scanner.Scan() {
		if strings.TrimSpace(scanner.Text()) != "" {
			count++
		}
	}
	return count, scanner.Err()
}

func main() {
	root, _ := os.Getwd()
	if filepath.Base(root) == "tools" {
		root = filepath.Dir(root)
	}
	languages, err := verify(root, "언어", "locale.conf")
	if err != nil {
		panic(err)
	}
	countries, err := verify(root, "나라", "country.conf")
	if err != nil {
		panic(err)
	}
	languageIndex, err := indexLines(filepath.Join(root, "언어-카탈로그.tsv"))
	if err != nil {
		panic(err)
	}
	countryIndex, err := indexLines(filepath.Join(root, "나라-카탈로그.tsv"))
	if err != nil {
		panic(err)
	}
	if languages != languageIndex || countries != countryIndex {
		panic(fmt.Sprintf("index mismatch: languages %d/%d countries %d/%d", languages, languageIndex, countries, countryIndex))
	}
	fmt.Printf("catalog OK: languages=%d countries=%d\n", languages, countries)
}
