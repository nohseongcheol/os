/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

// Command extract_identifier_words reports the English word components used by
// project-defined Go identifiers.  It deliberately ignores Go ABI/builtin
// names; the localization generator must leave those names intact.
package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
	"unicode"
)

func splitIdentifier(value string) []string {
	var result []string
	var current []rune
	runes := []rune(value)
	flush := func() {
		if len(current) != 0 {
			result = append(result, strings.ToLower(string(current)))
			current = nil
		}
	}
	for index, character := range runes {
		if character == '_' {
			flush()
			continue
		}
		if unicode.IsDigit(character) {
			flush()
			continue
		}
		if unicode.IsUpper(character) && len(current) != 0 {
			previousUpper := unicode.IsUpper(runes[index-1])
			nextLower := index+1 < len(runes) && unicode.IsLower(runes[index+1])
			if !previousUpper || nextLower {
				flush()
			}
		}
		current = append(current, character)
	}
	flush()
	return result
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: extract_identifier_words <localized name-correspondence.tsv>")
		os.Exit(2)
	}
	path := os.Args[1]
	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	words := map[string]int{}
	scanner := bufio.NewScanner(file)
	first := true
	for scanner.Scan() {
		if first {
			first = false
			continue
		}
		original := strings.SplitN(scanner.Text(), "\t", 2)[0]
		for _, word := range splitIdentifier(original) {
			words[word]++
		}
	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}
	ordered := make([]string, 0, len(words))
	for word := range words {
		ordered = append(ordered, word)
	}
	sort.Strings(ordered)
	for _, word := range ordered {
		fmt.Printf("%s\t%d\n", word, words[word])
	}
}
