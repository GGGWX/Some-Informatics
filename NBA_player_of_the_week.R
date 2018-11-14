library(ggplot2)
library(dplyr)
library(gridExtra)
library(RColorBrewer)
library(grid)
library(ggthemes)
library(ggrepel)
library(reshape2)
library(lubridate)
library(viridis)

#df <- read.csv('../NBA_player_of_the_week.csv', sep=',', stringAsFactors=FALSE)
df<-read.csv('./NBA_player_of_the_week.csv', sep=',', stringsAsFactors=F)

east_teams <- (df %>% filter(Conference == 'East') %>% distinct(Team))$Team
west_teams <- (df %>% filter(Conference == 'West') %>% distinct(Team))$Team

missingConference <- function(conf, team){
  if(conf == ''){
    if(team %in% east_teams | team == 'Washington Bullets'){
      return('East')
    }
    else if(team %in% west_teams | team == 'Washington Bullets'){
      return('West')
    }
  }
  else{
    return(conf)
  }
}

df$Conference_2 <- mapply(missingConference, df$Conference, df$Team)

heightNum <- function(x){
  if(grepl('cm', x) == TRUE){
    return(as.numeric(gsub('cm', '', x)))
  }
  else{
    foot = as.numeric(strsplit(x, '-')[[1]][1])
    inches = as.numeric(strsplit(x, '-')[[1]][2])
    return((foot * 12 + inches) * 2.54)
  }
}

weightNum <- function(x){
  if(grepl('kg', x) == TRUE){
    return(as.numeric(gsub('kg', '', x)))
  }
  else{
    return(as.numeric(x) * 0.453592)
  }
}

df$Height2 <- sapply(df$Height, heightNum)
df$Weight2 <- sapply(df$Weight, weightNum)
df$BMI <- df$Weight2 / ((df$Height2 / 100) * (df$Height2 / 100))


pos <- c("PG", "SG", "F", "C", "SF", "PF", "G", "FC", "GF", "F-C", "G-F")
posNames <- c("point guard","shooting guard","forward","center","small forward","power forward", "guard", "forward center","guard forward", "forward center", "guard forward")

df$position_name <- sapply(df$Position, function(x) posNames[match(x, pos)])

names <- c('guard','point guard','shooting guard','guard forward','forward','small forward','power forward','center','forward center')
colors <- c('#DC143C','#DC143C','#C71585','#C71585','#4682B4','#4682B4','#27408B','#006400','#006400')
COLOR <- data.frame(position_name = names, colors)
COLOR$position_name <- as.character(COLOR$position_name)

date <- function(x){
  current_date <- strsplit(x, ',')[[1]]
  current_year <- trimws(current_date[2])
  current_month <- match(strsplit(current_date[1], ' ')[[1]][1], month.abb)
  current_day <- strsplit(current_date[1], ' ')[[1]][2]
  return(paste0(current_year, '-', current_month, '-', current_day))
}

df$Date2 <- sapply(df$Date, date)
df$Date2 <- as.Date(df$Date2)
df$week <- as.integer(format(df$Date2, "%W")) + 1
df$day <- factor(weekdays(df$Date2, T), levels = rev(c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")))
df$month_num <- month(df$Date2)
df$month_name <- sapply(df$month_num, function(x) month.abb[x])

left_join(df %>% rename('HEIGHT(cm)' = Height2,
                        'WEIGHT(kg)' = Weight2) %>%
            select(position_name, 'HEIGHT(cm)', 'WEIGHT(kg)', BMI) %>%
            group_by(position_name) %>%
            reshape2::melt(id='position_name'),
          COLOR, by='position_name') %>%
  ggplot(aes(x = reorder(position_name, value, FUN = mean), y = value)) + 
  geom_boxplot(aes(fill = colors)) +
  theme_fivethirtyeight(12) +
  theme(legend.position = 'None',
        strip.text = element_text(size = 10, face = 'bold')) +
  scale_fill_identity() + facet_wrap(~variable, ncol = 1, scales = 'free')

left_join(
  df %>% group_by(Season.short, position_name) %>% summarise(meanHeight = mean(Height2)), 
  COLOR, by='position_name') %>% 
  ggplot(aes(x=Season.short, y= meanHeight, group=position_name)) + 
  geom_line(aes(color=colors),alpha=.75, size=2) + geom_point(size=2) + 
  theme_fivethirtyeight(12) +
  geom_smooth(aes(group=position_name),
              method='loess',alpha=.2,color='black',size=.25) +
  facet_wrap(~position_name) + scale_color_identity() +
  theme(strip.text = element_text(size = 10, face="bold")) + 
  labs(title='average Height over time per Position',
       subtitle='')





