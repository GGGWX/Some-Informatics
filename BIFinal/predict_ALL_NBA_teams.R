library(dplyr)
library(ggplot2)
library(randomForest)
library(arm)
library(stringr)
library(gridExtra)
library(formattable)
library(corrplot)

allnba <- read.csv('./input/All.NBA.1984-2018.csv', stringsAsFactors = F, header = T, skip = 1)
nbaplayers <- read.csv('./input/Seasons_Stats.csv', stringsAsFactors = F, header = T)
# dim(allnba)
# dim(nbaplayers)
# head(allnba)
# head(nbaplayers)

allnba$Year <- as.numeric(substr(allnba$Season, start = 1, stop = 4)) + 1
head(allnba[c(1:10), c(3, 34)], 10)
nbaplayers98 <- nbaplayers %>% filter(Year > 1998)
allnba98 <- allnba %>% filter(Year > 1998 & Year < 2018)

sum(is.na(nbaplayers98))

nbaplayers98$blanl <- NULL
nbaplayers98$blank2 <- NULL
colSums(is.na(nbaplayers98))

identical(which(is.na(nbaplayers98$PER)), which(is.na(nbaplayers98$USG.)))
which(is.na(nbaplayers98$PER))
nbaplayers98[c(3819, 4136, 5099, 6069, 7957), ]

nbaplayers98 <- nbaplayers98[-c(3819, 4136, 5099, 6069, 7957), ]

nbaplayers98[c(9429:9431), ]
nbaplayers98 <- subset(nbaplayers98, !Tm == "TOT")
which(allnba98$Tm == "TOT")
allnba98[239, 5] <- "ATL"
allnba98[180, 5] <- "DEN"
# merge players who are traded during a season
stats <- nbaplayers98 %>% mutate(Name = Player, Position = Pos, 
                                 age = Age, year = Year,  Team = Tm, Games = G, 
                                 Starts = GS, Minutes = MP/G, Points = PTS/G,
                                 Rebounds = TRB/G, Assists = AST/G, Steals = STL/G, 
                                 Blocks = BLK/G, Turnovers = TOV/G, Fouls = PF/G, 
                                 FTs = FT/G, Threes = X3P/G, FGs = FG/G, Usage = USG., 
                                 EfficiencyRating = PER, BoxPlusMinus = BPM, ShootingPercentage = eFG.)
# get stats per game
stats <- stats[ , c(52:73)]
twoDigitRound <- function(x) round(x, 2)
stats[ , c(8:18)] <- sapply(stats[ , c(8:18)], twoDigitRound)
str(stats)

stats <- stats %>% filter(Games > 10 & Minutes >5)

stats$ID <- str_c(substr(stats$Name, start = 1, stop = 3), 
                  substr(stats$age, start = 1, stop = 2),
                  substr(stats$Team, start = 1, stop = 3), 
                  substr(stats$year, start = 3, stop = 4), sep = "")
allnba98$ID <- str_c(substr(allnba98$Player, start = 1, stop = 3), 
                     substr(allnba98$Age, start = 1, stop = 2),
                     substr(allnba98$Tm, start = 1, stop = 3),
                     substr(allnba98$Year, start = 3, stop = 4), sep = "")
stats$All.NBA <- ifelse(stats$ID %in% allnba98$ID, 1, 0)
sum(stats$All.NBA)

check <- stats %>% filter(All.NBA == 1) %>% group_by(year) %>% summarise(length(Name))
check
stats[stats$year == 2013 & stats$All.NBA == 1, ]

stats[6047, 24] <- 0


# points_density <- ggplot(stats, aes(Points)) + geom_density(fill = "skyblue") + geom_vline(aes(xintercept = mean(Points)), linetype = "dashed")
# rebounds_density <- ggplot(stats, aes(Rebounds)) + geom_density(fill = "mediumorchid1") + geom_vline(aes(xintercept = mean(Rebounds)), linetype = "dashed")
# assists_density <- ggplot(stats, aes(Assists)) + geom_density(fill = "tomato") + geom_vline(aes(xintercept = mean(Assists)), linetype = "dashed")
# turnovers_density <- ggplot(stats, aes(Turnovers)) + geom_density(fill = "mediumaquamarine") + geom_vline(aes(xintercept = mean(Turnovers)), linetype = "dashed")
# grid.arrange(points_density, rebounds_density, assists_density, turnovers_density, ncol = 2)
# 
# stats$All.NBA <- as.factor(stats$All.NBA) 
# 
# log.points <- glm(All.NBA ~ Points, family = binomial, data = stats) ## run logit
# points.probability <- data.frame(Points = seq(0, 40, 0.1)) ## build basis of dataframe to predict probability at each 0.1 point interval
# points.prediction <- predict(log.points, points.probability, type = "response") ## run prediction based on logit
# points.probability <- cbind(points.probability, points.prediction)
# names(points.probability) <- c("Points", "Probability") 
# points.gg <- ggplot(points.probability, aes(Points, Probability)) + geom_line() + geom_vline(xintercept = mean(stats$Points), colour = "deepskyblue", linetype = "dashed") + geom_vline(xintercept = quantile(stats$Points, 0.99), colour = "sienna2", linetype = "dashed") + annotate("text", x = 24, y = 0.8, label = "99th percentile", angle = 90, colour = "sienna2", size = 3) + annotate("text", x = 7, y = 0.8, label = "Mean average", angle = 90, colour = "deepskyblue", size = 3)  ## build graph
# ## Now repeat for rebounds, assists and efficiency
# 
# ## rebounds
# log.rebounds <- glm(All.NBA ~ Rebounds, family = binomial, data = stats)
# rebounds.probability <- data.frame(Rebounds = seq(0, 25, 0.1))
# rebounds.prediction <- predict(log.rebounds, rebounds.probability, type = "response") 
# rebounds.probability <- cbind(rebounds.probability, rebounds.prediction)
# names(rebounds.probability) <- c("Rebounds", "Probability") 
# rebounds.gg <- ggplot(rebounds.probability, aes(Rebounds, Probability)) + geom_line() + geom_vline(xintercept = mean(stats$Rebounds), colour = "deepskyblue", linetype = "dashed") + geom_vline(xintercept = quantile(stats$Rebounds, 0.99), colour = "sienna2", linetype = "dashed") + annotate("text", x = 10.5, y = 0.75, label = "99th percentile", angle = 90, colour = "sienna2", size = 3) + annotate("text", x = 3, y = 0.75, label = "Mean average", angle = 90, colour = "deepskyblue", size = 3) 
# 
# ## assists
# log.assists <- glm(All.NBA ~ Assists, family = binomial, data = stats)
# assists.probability <- data.frame(Assists = seq(0, 20, 0.1))
# assists.prediction <- predict(log.assists, assists.probability, type = "response") 
# assists.probability <- cbind(assists.probability, assists.prediction)
# names(assists.probability) <- c("Assists", "Probability") 
# assists.gg <- ggplot(assists.probability, aes(Assists, Probability)) + geom_line() + geom_vline(xintercept = mean(stats$Assists), colour = "deepskyblue", linetype = "dashed") + geom_vline(xintercept = quantile(stats$Assists, 0.99), colour = "sienna2", linetype = "dashed") + annotate("text", x = 8, y = 0.75, label = "99th percentile", angle = 90, colour = "sienna2", size = 3) + annotate("text", x = 1.2, y = 0.75, label = "Mean average", angle = 90, colour = "deepskyblue", size = 3) 
# 
# ## PER
# log.PER <- glm(All.NBA ~ EfficiencyRating, family = binomial, data = stats)
# PER.probability <- data.frame(EfficiencyRating = seq(0, 40, 0.1))
# PER.prediction <- predict(log.PER, PER.probability, type = "response")
# PER.probability <- cbind(PER.probability, PER.prediction)
# names(PER.probability) <- c("PER", "Probability")
# PER.gg <- ggplot(PER.probability, aes(PER, Probability)) + geom_line() + geom_vline(xintercept = mean(stats$EfficiencyRating), colour = "deepskyblue", linetype = "dashed") + geom_vline(xintercept = quantile(stats$EfficiencyRating, 0.99), colour = "sienna2", linetype = "dashed") + annotate("text", x = 24, y = 0.9, label = "99th percentile", angle = 90, colour = "sienna2", size = 3) + annotate("text", x = 11, y = 0.9, label = "Mean average", angle = 90, colour = "deepskyblue", size = 3) 
# 
# ## print graphs
# grid.arrange(points.gg, rebounds.gg, assists.gg, PER.gg, top = "The probability of being selected for the All NBA teams, at different levels of output")

statsCor <- as.matrix(stats[ , c(6:20)])
corrplot(cor(statsCor), method = "circle", type = "upper")

stats$ShootingPercentage <- stats$ShootingPercentage * 100
multiVariable <- glm(All.NBA ~ Points + Rebounds + Assists + Usage + ShootingPercentage + Steals + Blocks + Turnovers + Fouls + FTs, family = binomial, stats)
summary(multiVariable)
multiVariable_2 <- round(exp(cbind(Odds_Ratio = coef(multiVariable), confint(multiVariable))), 3)
formattable(multiVariable_2)
summary(multiVariable_2)


training <- stats %>% filter(year < 2012)
testing <- stats %>% filter(year >= 2012)
# dim(training)
# dim(testing)

set.seed(100)
model <- randomForest(All.NBA ~ Points + Assists + Rebounds + age + Games + Starts + Minutes + Steals + Blocks + Turnovers + Fouls + FTs + Threes + FGs + Usage + EfficiencyRating + BoxPlusMinus + ShootingPercentage, data = training)
plot(model)
varImpPlot(model)
# use random forest to train our data

modelPredict <- predict(model, testing, type = "response")
testingCheck <- data.frame(cbind(testing, modelPredict))
testingCheck$TruePositive <- ifelse(testingCheck$All.NBA == 1 & testingCheck$modelPredict == 1, 1, 0)
testingCheck$TrueNegative <- ifelse(testingCheck$All.NBA == 0 & testingCheck$modelPredict == 0, 1, 0)
testingCheck$FalseNegative <- ifelse(testingCheck$All.NBA == 1 & testingCheck$modelPredict == 0, 1, 0)
testingCheck$FalsePositive <- ifelse(testingCheck$All.NBA == 0 & testingCheck$modelPredict == 1, 1, 0)
results <- c(sum(testingCheck$TruePositive), sum(testingCheck$TrueNegative), sum(testingCheck$FalsePositive), sum(testingCheck$FalseNegative))
predictions <- data.frame(cbind(c("True Positive", "True Negative", "False Positive", "False Negative"), results))
predictions$results <- as.numeric(as.character(predictions$results))
names(predictions) <- c("Type", "Count")
formattable(predictions)
# Binary prediction