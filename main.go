package main

import (
	"encoding/json"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"os"
	"path/filepath"
)

var (
	validChannels = map[string]struct{}{
		"channelA": {},
		"channelB": {},
	}
)

func main() {
	r := setupRouter()
	// Listen and Server in 0.0.0.0:8080
	r.Run(":8080")
}

func setupRouter() *gin.Engine {
	// Disable Console Color
	// gin.DisableConsoleColor()
	r := gin.Default()

	// health check test
	r.GET("/healthcheck", func(c *gin.Context) {
		c.String(http.StatusOK, "")
	})

	// v1 channels API to fetch details pertaining to a channelID
	r.GET("/v1/channels/:channel_id", func(c *gin.Context) {
		// getting the passed in param
		channelID := c.Params.ByName("channel_id")

		// getting the present working directory
		projectDir, err := os.Getwd()
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{})
			return
		}

		// get the parent directory as it is running inside the cucumber sub-directory.
		parentDir := filepath.Dir(projectDir)
		channelDataPath := fmt.Sprintf("data/%s/get.json", channelID)
		filePath := filepath.Join(parentDir, channelDataPath)

		// as the file is small we are using os.Readfile,
		// else we can use os.Open as well with json decoder in conjunction
		file, err := os.ReadFile(filePath)
		if err != nil {
			// using anonymous struct here, we can create concrete struct as well.
			resp := struct {
				Err string `json:"error"`
			}{
				Err: "channel not found",
			}

			jsonData, _ := json.Marshal(resp)
			c.Data(http.StatusNotFound, "application/json", jsonData)
			return
		}

		// Decode JSON into a map
		var result map[string]interface{}
		err = json.Unmarshal(file, &result)
		if err != nil {
			fmt.Printf("Error decoding file to JSON: %v\n", err)
			c.JSON(http.StatusInternalServerError, gin.H{})
			return
		}

		// convert read JSON back to JSON to return.
		jsonData, err := json.Marshal(result)
		if err != nil {
			fmt.Printf("Error marshalling JSON: %v\n", err)
			c.JSON(http.StatusInternalServerError, gin.H{})
			return
		}

		c.Data(http.StatusOK, "application/json", jsonData)
	})

	r.GET("/v2/channels/:channel_id", func(c *gin.Context) {
		channelID := c.Params.ByName("channel_id")

		if _, ok := validChannels[channelID]; !ok {
			resp := struct {
				Err string `json:"error"`
			}{
				Err: "internal server error",
			}

			jsonData, _ := json.Marshal(resp)
			c.Data(http.StatusInternalServerError, "application/json", jsonData)
			return
		}

		projectDir, err := os.Getwd()
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{})
			return
		}

		// get the parent directory as it is running inside the cucumber project.
		parentDir := filepath.Dir(projectDir)
		channelDataPath := fmt.Sprintf("data/%s/get_v2.json", channelID)
		filePath := filepath.Join(parentDir, channelDataPath)

		file, err := os.ReadFile(filePath)
		if err != nil {
			resp := struct {
				Err string `json:"error"`
			}{
				Err: "channel not found",
			}

			jsonData, _ := json.Marshal(resp)
			c.Data(http.StatusNotFound, "application/json", jsonData)
			return
		}

		// Decode JSON into a map
		var result map[string]interface{}
		err = json.Unmarshal(file, &result)
		if err != nil {
			fmt.Printf("Error decoding file to JSON: %v\n", err)
			c.JSON(http.StatusInternalServerError, gin.H{})
			return
		}

		// convert read JSON back to JSON to return.
		jsonData, err := json.Marshal(result)
		if err != nil {
			fmt.Printf("Error marshalling JSON: %v\n", err)
			c.JSON(http.StatusInternalServerError, gin.H{})
			return
		}

		c.Data(http.StatusOK, "application/json", jsonData)
	})

	return r
}
