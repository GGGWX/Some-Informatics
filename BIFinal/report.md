# Final project for Business Intelligence course

## Descriptive Analysis

### 1-1. Method

In this part, I mainly focus on the data cleaning, data visualization, and some simple regressions to help illustrate some cool facts.

### 2-1. Summary

In this kernel, what I am going to do is tp predict something using linear regression model, and here are some key questions:

1. Which indicators are most associated with a player's salary?
2. How to deal with multiple datasets?
3. How to describe my findings through data visualization?

### 2-2. About NBA salary

Much different from the LEAGUEs like La Liga or Premier League, NBA has a very complicated principle for its players. At the very first I want using the data provided by NBA official to divide players into a training set and a testing set. But then I found that many players are provided with a long-term contract, increasing yearly. Very few of them get one-year contracts. With lots of disadvantages, I change my topic to focus on analyzing statistics to see what is/are important for a player to get higher salary and make a simple prediction.

### 3. Preparing the data

Using a python spider to get players' salary from [basketball-reference](https://www.basketball-reference.com/contracts/players.html), and download players' stats from its official website.

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.43.06.png)

A lot of missing data, but never mind, we only need one year data. And since there are no average stats in this dataset, just figure them out and merge.

### 4. Correlation rule

#### 4-1. First rule

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.43.55.png)

And the plot is shown above, we can roughly see that Points Per Game(PPG) has a higher weight with APG following.

#### 4-2. Second rule

```R
stats_salary_2 <- stats_salary %>%
  select(salary17_18, PPG, MPG, APG, RPG, PER, SPG, TOPG)
ggpairs(stats_salary_2, mapping = ggplot2::aes(color = "red"))
```

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.44.28.png)

We can see the correlation strength is that: PPG>MPG>TOPG>RPG>PER>SPG>APG.

To my surprise, the PER value is not a very crucial factor to a player's salary, although it is a very important statistic overly mentioned in the past years. And TOPG is a very interesting indicator, which means TurnOver Per Game. If a player has higher TOPG, this may imply that one has more time taking the ball in controll, or has to face more intensive defence, which means that he is important to his team. So maybe more turnovers stands for higher salary.

### 5. Regression analysis

#### 5-1. Single linear regression

```R
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
```

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.46.40.png)

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.47.19.png)

As you can see, if I take PER as an indicator, it does have some drawbacks. Here is a distinct outlier: he has a very high PER but is assigned a base pay at $50000. This may arise from the formula of PER, which does not weight enough on a player's play time. So let's see what does PPG do with salary.

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.45.02.png)

Much better, right? If we hover our mouse on any point, it will show the player name and PPG. Stephen Curry gets the highest paid, because he had a new contracts at 2016 summer.

```R
stats_salary %>%
  ggplot(aes(x = salary17_18, y = PPG)) +
  geom_point(aes(alpha = 0.8), size = 1.2)+
  geom_smooth(method = "lm")
```

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.47.55.png)

```R
regression <-
stats_salary %>% select(salary17_18, MPG:SPG)
lm(salary17_18~., data = regression)
```

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.48.25.png)

Points per game increases $686815 per year, but assists per game even increases \$1059087 per year! No wonder that many PGs are highly paid.

#### 5-2. Parallel model

We add two new indicators: average play time and average turnovers.(per game) And we say a player is trusted if he plays more time than the average, a player is important if he has more turnovers than the average.

```R
avgMPG <- mean(regression$MPG)
avgTOPG <- mean(regression$TOPG)
regression$trust <- as.factor(ifelse(regression$MPG >= avgMPG, "yes", "no"))
regression$imp <- as.factor(ifelse(regression$TOPG >= avgTOPG, "yes", "no"))
regression %>%
  ggplot(aes(x = salary17_18, y = PPG, color = imp)) +
  geom_point() +
  geom_smooth(method = "lm")
```

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.49.48.png)

```R
regression_2 <- lm(formula = salary17_18 ~ imp * trust, data = regression)
summary(regression_2)
```

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.50.13.png)

### Conclusion

Let's take a player with one-year contract as an example to see how much he will get in the next year.

```R
prediction <- function(m, point, minutes, turnover){
  new <- predict(m, data.frame(PPG = point, MPG = minutes, TOPG = turnover))
  msg <- paste("PPG:", point, "MPG:", minutes, "TOPG:", turnover, " -> Expected salary: $",
               format(round(new), big.mark = ","), sep = "")
  print(msg)
}
model <- lm(formula = salary17_18 ~ PPG + MPG + TOPG, data = regression)
# input stats to see salary
prediction(model, 27.5, 36.9, 3.0)# LeBron James
```

And the result is $21,768,949, much less than \$35,654,150. So this regression is not proper for those superstars. Because NBA is a LEAGUE weighing a lot on commercial value. Let's take another example.

```R
prediction(model, 18.0, 25.0, 3.0)# Jeremy Lin
```

The result is $13,329,357, and this year Jeremy gets \$13,768,421. Nearly the same. But not enough.

## Predictive Analysis

### 1. Method

In this part, I focus on the data cleaning, data visualization, multivariate logistic regressions and prepare a training dataset with a testing dataset using random forest algorithm to finish predicting task.

### 2-1. Summary

In this kernel, here are some key questions:

1. Which indicators are most associated with selection to the All NBA team?
2. To what extent can a machine learning algorithm predict selection?
3. Where does this algorithm differ from observed selection and why?

### 2-2. About the All NBA team

Each year in the NBA, only 15 players are selected to the All NBA teams. This process is done by a vote from 100 authoritative journalists. The All NBA teams award is a supreme pride for those players: less than 3% of players will be selected.

### 3.Preparing the data

In this part, I tidy the dataset from for NBA players during year 1998-2017.

```R
allnba <- read.csv('./input/All.NBA.1984-2018.csv', stringsAsFactors = F, header = T, skip = 1)
nbaplayers <- read.csv('./input/Seasons_Stats.csv', stringsAsFactors = F, header = T)
dim(allnba)
dim(nbaplayers)
head(allnba)
head(nbaplayers)
```

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.51.23.png)

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午8.51.45.png)

As we can see, our main dataset is very large, having nearly 25000 rows with 53 columns each, has a lot of missing data, the NA values. Now we will make the data more useful.

#### 3-1. Eliminate ambiguity

In this part we are focusing on year 1998 - 2017. Because the quality of the data are higher and more comprehensive than previous time. Also, basketball of this period is more modernized, that is, meaningful and familiar to us. Additionally, 'Year' and 'Season' are two different concepts in NBA, so we need eliminate this ambiguity. We make Season 1990-91 equal to Year 1991.

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午9.00.06.png)

#### 3-2. Data cleaning

Then we need to deal with the NA value. I used the same data in the previous analysis, but I did not dispose the missing data, now I'm checking for it.

```R
sum(is.na(nbaplaers98))
# 24225
nbaplayers98$blanl <- NULL
nbaplayers98$blank2 <- NULL
colSums(is.na(nbaplayers98))
```

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午9.12.08.png)

As expected, we eliminate these two blank tuples then we have much less missing data. It is tolerant that some stats are missing, because they may not get any in their career, like X3P., which means 3-point shot percentage. But PER, an impoertant indicator we used in the previous part, have 5 data missing. Now we will find out why PER are missing.

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午9.18.42.png)

Why PER are missing? Because they did not get enough play time so that they did not get enough stats to be taken into account in PER formula. So we drop out these data.

```R
nbaplayers98 <- nbaplayers98[-c(3819, 4136, 5099, 6069, 7957), ]
```

Also, if one player is traded to another team during the Season, there will be two rows for separate stats and a row for the total stats. So we just need to merge them together.

```R
nbaplayers98 <- subset(nbaplayers98, !Tm == "TOT")
```

You must remember last analysis we got a dataset of stats per-game, we also need to do this in the current analysis.

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午9.33.29.png)

In addition, as we mention before, we need a dataset without players who only played a few games in a season. We call them outliers, which are not helpful in our prediction: waste our time and lower the accuracy of our predictive.

```R
stats <- stats %>% filter(Games > 10 & Minutes >5)
```

### 4. Analysis

#### 4-1. Density graphs

As I mentioned above, NBA is a LEAGUE of superstars. A best player can often determine the win or loss. We take points, rebounds, assists and turnovers as out indicators to see the output. We can see that the **skewness** of the graphs are positive, with a long trail from **the mean** away from **the median**. GGplot helps us see the graph clearly.

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午9.51.19.png)

#### 4-2. Correlation rule

```R
statsCor <- as.matrix(stats[ , c(6:20)])
corrplot(cor(statsCor), method = "circle", type = "upper")
```

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午10.07.37.png)

Feels very familiar, right? We draw a similar plot before, but this one has more variables to help us to find out more precise correlation rules.

### 5-1. Multivariable logistic regression

Before we go to the machine learning part, let's see some differences between **univariate logistic regression (in descriptive analysis) and multivariate logistic regressions**.

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午10.19.55.png)

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午10.13.17.png)

As you can see: the minimal adequate logistic model can reduce deviance from 2493 points in the null model to 711 in our model, with the loss of just degrees of freedom. The odds ratios show us the relative effect of each factor. Odds ratios are a little different than standard regression coefficients. For example, in the above, the odds of being selected as All NBA are 3.5 times greater.

### 6. Using Random Forest algorithm

Using a random forest to predict is a totally new and challenging part different from my previous ***"salary prediction"***, because All NBA team is more predictable and we have more indicators to help predict more accurate. You can see that we use randomForest model can help us reduce the error to 0.012(2674 True Negative/ 2689 all players). And I use something learned from our class([reference](https://blog.csdn.net/sinat_26917383/article/details/51308061)), which is quite helpful.

![](/Users/gggwx/Desktop/屏幕快照 2018-12-06 下午7.58.59.png)

![](/Users/gggwx/Desktop/屏幕快照 2018-12-06 下午3.10.59.png)

![](/Users/gggwx/Desktop/屏幕快照 2018-12-05 下午10.35.10.png)

![](/Users/gggwx/Desktop/屏幕快照 2018-12-06 下午8.00.52.png)

## Epilogue

In this project, I mainly focus on data visualization and some simple linear regression. After reading some tutorial codes on kaggle, I tried to use some more complex methods to do predictive analysis. And I tried something new using R language, because R has its advantages in descriptive aspects. In order to save place, I left out some codes and mainly put images in my report. For more details just see my source code with comments. Thanks to Business Intelligence course, I pushed myself to learn a new language **R** and a new website **kaggle** for me to get well-organized data. Also the project helped me review how to write a **python** crawler. XD

## Reference

[Randon Forests(2001), by Leo Breiman](https://link.springer.com/article/10.1023/A:1010933404324)

[kaggle](https://www.kaggle.com)

[R for Data Science](https://r4ds.had.co.nz/introduction.html)