package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"gopkg.in/yaml.v3"
)

// Command-line argument parsing
var key = flag.String("key", "", "Key to be updated")
var value = flag.String("value", "", "New value for the key")
var env = flag.String("env", "", "Environment")

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

// Function to search for a key within YAML file and return the value when found
func searchKeyValue(file string, key string) (interface{}, error) {
	content, err := os.ReadFile(file)
	if err != nil {
		return nil, err
	}
	var yamlContent interface{}
	err = yaml.Unmarshal(content, &yamlContent)
	if err != nil {
		return nil, err
	}
	value := searchValue(yamlContent, key)
	return value, nil
}

// Recursive function to search for a key within YAML structure and return the value when found
func searchValue(obj interface{}, key string) interface{} {
	// Split the key if it contains a delimiter
	keys := strings.Split(key, ".")
	var parentKey, childKey string

	if len(keys) > 1 {
		parentKey = keys[0]
		childKey = keys[1]
	} else {
		childKey = key
	}

	switch obj := obj.(type) {
	case map[string]interface{}:
		if parentKey != "" {
			// If there's a parent key, find the parent first
			if parentObj, ok := obj[parentKey]; ok {
				// Now search for the child key within the parent object
				return searchValue(parentObj, childKey)
			}
		} else {
			// No parent key, search directly in the current map
			for k, v := range obj {
				if k == childKey {
					return v
				}
				// Recursively search for the child key
				value := searchValue(v, childKey)
				if value != nil {
					return value
				}
			}
		}
	case []interface{}:
		// If it's an array, iterate and search for the key in each item
		for _, item := range obj {
			value := searchValue(item, key)
			if value != nil {
				return value
			}
		}
	}
	return nil
}

func main() {
	flag.Parse()

	args := flag.Args()
	if len(args) == 0 {
		log.Fatal("Please provide a subcommand: search or replace")
	}
	subcommand := args[0]

	switch subcommand {
	case "get-database-host":
		if *env == "" {
			log.Fatal("Please input the env for database!")
		}

		workingDir, err := os.Getwd()
		if err != nil {
			log.Fatal(err)
		}
		var files []string
		switch *env {
		case "prod":
			files = append(files, filepath.Join(workingDir, "dbs", "db_prod.yaml"))
		case "stg":
			files = append(files, filepath.Join(workingDir, "dbs", "db_stg.yaml"))
		default:
			log.Fatalf("Invalid environment: %s", *env)
		}
		for _, file := range files {
			value, err := searchKeyValue(file, "host")
			if err != nil {
				log.Fatalf("Failed to search key: %v", err)
			}
			if value != nil {
				fmt.Printf("%v\n", value)
			}
		}

	case "replace":

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

	default:
		log.Fatalf("Invalid subcommand: %s", subcommand)
	}
}
