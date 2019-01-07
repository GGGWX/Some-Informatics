library(data.table)
library(corrplot)
library(GGally)
library(tidyverse)
library(PerformanceAnalytics)
library(plotly)
library(ggplot2)

salarytable <- read.csv("./input/NBA_season1718_salary.csv")
nbaplayers <- read.csv("./input/Seasons_Stats.csv")

# head(salarytable)
# head(nbaplayers)
# str(salarytable)
# str(nbaplayers)

stats17 <- 
  nbaplayers %>% filter(Year >= 2017) %>% 
  select(Year:G, MP, PER, FG:PTS) %>% 
  distinct(Player, .keep_all = TRUE) %>% 
  mutate(MPG = MP/G, PPG = PTS/G, APG = AST/G, 
         RPG = TRB/G, TOPG = TOV/G, BPG = BLK/G, 
         SPG = STL/G) 
# to get stats per game

stats_salary <- merge(stats17, salarytable, by.x = "Player", by.y = "Player")
head(stats_salary)
names(stats_salary)[40] <- "salary17_18"
stats_salary <- stats_salary[-39]
# merge two csv file to get a new dataset

corrplot(cor(stats_salary %>%
               select(salary17_18, MPG:SPG, Age, PER, contains("%")),
             use = "complete.obs"),
         method = "circle", type = "upper")
# plot 1, find correlation between some stats

stats_salary_2 <- stats_salary %>%
  select(salary17_18, PPG, MPG, APG, RPG, PER, SPG, TOPG)
ggpairs(stats_salary_2, mapping = ggplot2::aes(color = "red"))
# plot 2, find another correaltion


# ggscatmat(salarytable, alpha = 0.3, corMethod = "pearson")
# a simple scatter chart to roughly see 
# the relation between discrete data

# cor(stats_salary_2)[, "salary17_18"]
# to verify the correlation

names(stats_salary)[5] <- "Team"
plot_ly(data = stats_salary, x = ~salary17_18, y = ~PER, color = ~Team,
        hoverinfo = "text",
        text = ~paste("Player: ", Player,
                      "<br>Salary: ", format(salary17_18, big.mark = ","),"$",
                      "<br>PER: ", round(PER, digits = 1),
                      "<br>Team: ", Team)) %>% 
  layout(
    title = "Salary vs PER",
    xaxis = list(title = "Salary/$"),
    yaxis = list(title = "PER")
  )

stats_salary %>%
  ggplot(aes(x = salary17_18, y = PPG)) +
  geom_point(aes(alpha = 0.8), size = 1.2)+
  geom_smooth(method = "lm")

regression <-
  stats_salary %>% select(salary17_18, MPG:SPG)
lm(salary17_18~., data = regression)

avgMPG <- mean(regression$MPG)
avgTOPG <- mean(regression$TOPG)
regression$trust <- as.factor(ifelse(regression$MPG >= avgMPG, "yes", "no"))
regression$imp <- as.factor(ifelse(regression$TOPG >= avgTOPG, "yes", "no"))

regression %>%
  ggplot(aes(x = salary17_18, y = PPG, color = imp)) +
  geom_point() +
  geom_smooth(method = "lm")

regression_2 <- lm(formula = salary17_18 ~ imp * trust, data = regression)
summary(regression_2)

prediction <- function(m, point, minutes, turnover){
  new <- predict(m, data.frame(PPG = point, MPG = minutes, TOPG = turnover))
  msg <- paste("PPG:", point, "MPG:", minutes, "TOPG:", turnover, " -> Expected salary: $",
               format(round(new), big.mark = ","), sep = "")
  print(msg)
}
# this function can be extended to have more parameters
# to have a more accurate result for salary prediction

model <- lm(formula = salary17_18 ~ PPG + MPG + TOPG, data = regression)
# input stats to see salary

prediction(model, 27.5, 36.9, 3.0) # LeBron James
prediction(model, 18.0, 25.0, 3.0) # Jeremy Lin

