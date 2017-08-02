install.packages("httpuv")
library(httr)
library(httpuv)
oauth_endpoints("github")
myapp <- oauth_app("github",
                   key = "10702ebafa7e53377cc3",
                   secret = "d7a0835d57cb21df0f9c262ff61a8c7daa14ca49")
github_token <- oauth2.0_token(oauth_endpoints("github"), myapp)
gtoken <- config(token = github_token)
req <- GET("https://api.github.com/users/jtleek/repos", gtoken)
stop_for_status(req)
content(req)
