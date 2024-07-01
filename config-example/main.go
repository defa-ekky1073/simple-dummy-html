package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strconv"

	"gopkg.in/yaml.v3"
)

// Function to load YAML files from a directory
func loadYAMLFiles(directory string) ([]string, error) {
	var yamlFiles []string
	err := filepath.Walk(directory, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() && (filepath.Ext(path) == ".yaml" || filepath.Ext(path) == ".yml") {
			yamlFiles = append(yamlFiles, path)
		}
		return nil
	})
	return yamlFiles, err
}

// Function to read YAML file contents
func readYAMLContents(files []string) (map[string]interface{}, error) {
	yamlContents := make(map[string]interface{})
	for _, file := range files {
		content, err := os.ReadFile(file)
		if err != nil {
			return nil, err
		}
		var yamlContent interface{}
		err = yaml.Unmarshal(content, &yamlContent)
		if err != nil {
			return nil, err
		}
		yamlContents[file] = yamlContent
	}
	return yamlContents, nil
}

// Recursive function to update value in YAML structure
func updateValue(obj interface{}, key string, newValue interface{}) interface{} {
	switch obj := obj.(type) {
	case map[string]interface{}:
		for k, v := range obj {
			if k == key {
				obj[k] = newValue
			} else {
				obj[k] = updateValue(v, key, newValue)
			}
		}
	case []interface{}:
		for i, item := range obj {
			obj[i] = updateValue(item, key, newValue)
		}
	}
	return obj
}

// Function to replace key-value pairs in YAML files and save them
func replaceKeyValue(file string, contents interface{}, key string, value interface{}) error {
	updatedValue := updateValue(contents, key, value)
	updatedYAML, err := yaml.Marshal(updatedValue)
	if err != nil {
		return err
	}
	err = os.WriteFile(file, updatedYAML, 0644)
	return err
}

func main() {
	// Command-line argument parsing
	key := flag.String("key", "", "Key to be updated")
	value := flag.String("value", "", "New value for the key")
	flag.Parse()

	if *key == "" || *value == "" {
		log.Fatal("Please input the key and value you want to change!")
	}

	// Input validator
	var argsValue interface{} = *value
	if intValue, err := strconv.Atoi(*value); err == nil {
		argsValue = intValue
	} else if *value == "true" {
		argsValue = true
	} else if *value == "false" {
		argsValue = false
	}

	workingDir, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}

	files, err := loadYAMLFiles(workingDir)
	if err != nil {
		log.Fatal(err)
	}

	contents, err := readYAMLContents(files)
	if err != nil {
		log.Fatal(err)
	}

	for file, content := range contents {
		err := replaceKeyValue(file, content, *key, argsValue)
		if err != nil {
			log.Fatalf("Failed to replace file: %v", err)
		}
		fmt.Printf("Successfully updated key `%s` to `%v` value\n", *key, argsValue)
	}
}
