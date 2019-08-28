options(warn=-1)

if("rtweet" %in% rownames(installed.packages()) == FALSE) {
	message("rtweet not installed - Exiting")
	quit()
}
if("jsonlite" %in% rownames(installed.packages()) == FALSE) {
	message("jsonlite not installed - Exiting")
	quit()
}

# Load packages
suppressMessages(library(rtweet))
suppressMessages(library(jsonlite))

# Set args
args = commandArgs(trailingOnly=TRUE)

# Read tokens from json and write to RDS
tokens_json <- jsonlite::read_json(args[1])
rtweet_tokens <- list()
for (token in tokens_json) {
  rtweet_token <- rtweet::create_token(app = "[APP_NAME]", 
                                       consumer_key = "[CONSUMER_KEY]", 
                                       consumer_secret = "[CONSUMER_SECRET]",
                                       access_token = token$token, 
                                       access_secret = token$secret,
                                       set_renv = FALSE)
  rtweet_tokens <- c(rtweet_tokens, rtweet_token)
}

message("Writing to rtweet_tokens.RDS")
saveRDS(rtweet_tokens, file = "rtweet_tokens.RDS")
