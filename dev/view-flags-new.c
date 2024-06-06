#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

#define LOCATION "/var/www's" 
#define PD_MESSAGE "\"Intruder!! "\
		LOCATION\
		" canary triggered\""
#define SLACK_MESSAGE "\"<!channel> Intruder!! "\
		LOCATION\
		" canary triggered\""


size_t write_data(void *buffer, size_t size, size_t nmemb, void *userp){ return CURLE_OK; }

void send_pagerduty_alert() {
    CURL *curl;
    CURLcode res;

    // Initialize libcurl
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if(curl) {
        const char *url = "https://events.pagerduty.com/v2/enqueue";
        const char *json_data = "{"
                                "\"payload\": {"
                                "\"summary\":"
				PD_MESSAGE	
				","
                                "\"severity\": \"critical\","
                                "\"source\": \"view-flags canary\""
                                "},"
                                "\"routing_key\": \"5524d5b5bb8c4902d0f8108c5c2a33ef\","
                                "\"event_action\": \"trigger\""
                                "}";

        // Set the URL and HTTP method to POST
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data);
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);

        // Set the Content-Type header
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Perform the request
        res = curl_easy_perform(curl);

        // Check for errors
	/*
        if(res != CURLE_OK) {
            fprintf(stderr, "PagerDuty request failed: %s\n", curl_easy_strerror(res));
        }
	*/

        // Clean up
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }

    // Global cleanup
    curl_global_cleanup();
}

void send_slack_notification() {
    CURL *curl;
    CURLcode res;

    // Initialize libcurl
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if(curl) {
        const char *url = "https://hooks.slack.com/services/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";
        const char *json_data = "{"
                                "\"text\":"
				SLACK_MESSAGE
                                "}";

        // Set the URL and HTTP method to POST
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_POST, 1L);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data);
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);

        // Set the Content-Type header
        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        // Perform the request
        res = curl_easy_perform(curl);

        // Check for errors
        /*
	if(res != CURLE_OK) {
            fprintf(stderr, "Slack request failed: %s\n", curl_easy_strerror(res));
        }
	*/

        // Clean up
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    }

    // Global cleanup
    curl_global_cleanup();
}

int main(void) {
    printf("Root flag: %s\n", "pZ7t8KJd2mNcWx5bQlH4");
    printf("Site flag: %s\n", "F2bRtL9jP0QvUzWkE3nA");
    /* printf("DB flag: %s\n", "5A9V6K3W2Y1R"); */

    send_pagerduty_alert(); 
    send_slack_notification();
    return 0;
}

