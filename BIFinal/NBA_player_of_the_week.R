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

df <- read.csv('./input/NBA_player_of_the_week.csv', sep=',', stringsAsFactors=F)

eastTeams <- (df %>% filter(Conference == 'East') %>% distinct(Team))$Team
westTeams <- (df %>% filter(Conference == 'West') %>% distinct(Team))$Team

missingConference <- function(conf, team){
  if(conf == ''){
    if(team %in% eastTeams | team == 'Washington Bullets'){
      return('East')
    }
    else if(team %in% westTeams | team == 'Washington Bullets'){
      return('West')
    }
  }
  else{
    return(conf)
  }
}

df$newConference <- mapply(missingConference, df$Conference, df$Team)

getHeight <- function(x){
  if(grepl('cm', x) == TRUE){
    return(as.numeric(gsub('cm', '', x)))
  }
  else{
    foot = as.numeric(strsplit(x, '-')[[1]][1])
    inches = as.numeric(strsplit(x, '-')[[1]][2])
    return((foot * 12 + inches) * 2.54)
  }
}

getWeight <- function(x){
  if(grepl('kg', x) == TRUE){
    return(as.numeric(gsub('kg', '', x)))
  }
  else{
    return(as.numeric(x) * 0.453592)
  }
}

df$newHeight <- sapply(df$Height, getHeight)
df$newWeight <- sapply(df$Weight, getWeight)
df$BMI <- df$newWeight / ((df$newHeight / 100) * (df$newHeight / 100))


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

df$newDate <- sapply(df$Date, date)
df$newDate <- as.Date(df$newDate)
df$week <- as.integer(format(df$newDate, "%W")) + 1
df$day <- factor(weekdays(df$newDate, T), levels = rev(c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")))
df$month_num <- month(df$newDate)
df$month_name <- sapply(df$month_num, function(x) month.abb[x])




# 
# left_join(df %>% rename('HEIGHT(cm)' = newHeight,
#                         'WEIGHT(kg)' = newWeight) %>%
#             select(position_name, 'HEIGHT(cm)', 'WEIGHT(kg)', BMI) %>%
#             group_by(position_name) %>%
#             reshape2::melt(id='position_name'),
#           COLOR, by='position_name') %>%
#   ggplot(aes(x = reorder(position_name, value, FUN = mean), y = value)) +
#   geom_boxplot(aes(fill = colors)) +
#   theme_fivethirtyeight(12) +
#   theme(legend.position = 'None',
#         strip.text = element_text(size = 10, face = 'bold')) +
#   scale_fill_identity() + facet_wrap(~variable, ncol = 1, scales = 'free')

# left_join(
#   df %>% group_by(Season.short, position_name) %>% summarise(meanHeight = mean(newHeight)),
#   COLOR, by='position_name') %>%
#   ggplot(aes(x=Season.short, y= meanHeight, group=position_name)) +
#   geom_line(aes(color=colors),alpha=.75, size=1) + geom_point(size=1) +
#   theme_fivethirtyeight(12) +
#   geom_smooth(aes(group=position_name),
#               method='loess',alpha=.2,color='black',size=.25) +
#   facet_wrap(~position_name) + scale_color_identity() +
#   theme(strip.text = element_text(size = 10, face="bold")) +
#   labs(title='average Height over time per Position',
#        subtitle='')

# left_join(
#   df %>% group_by(Season.short, position_name) %>% summarise(meanBMI = mean(BMI)), 
#   COLOR, by='position_name') %>% 
#   ggplot(aes(x=Season.short, y= meanBMI, group=position_name)) + 
#   geom_line(aes(color=colors),alpha=.75, size=2) + geom_point(size=2) + 
#   theme_fivethirtyeight(12) +
#   geom_smooth(aes(group=position_name),
#               method='loess',alpha=.2,color='black',size=.25) +
#   facet_wrap(~position_name) + scale_color_identity() +
#   theme(strip.text = element_text(size = 10, face="bold")) + 
#   labs(title='average BMI over time per Position',
#        subtitle='')

# unique_players <- df[!duplicated(df$Player), c('Player', 'position_name')]
# 
# left_join(
#   left_join(
#     df %>% select(newHeight, newWeight, BMI, position_name, Player) %>%
#       group_by(Player) %>%
#       summarise(
#         count=n(),
#         meanHeight = mean(newHeight),
#         meanWeight = mean(newWeight),
#         meanBMI = mean(BMI)) %>% arrange(-count),
#     unique_players, by='Player'),
#   COLOR, by='position_name') %>%
#   ggplot(aes(x=meanHeight, y=meanWeight)) +
#   geom_jitter(aes(color=colors, size=count), alpha = 0.5, width = 0.8, height = 0.8) +
#   theme_fivethirtyeight(12) + theme(legend.position = 'top') +
#   scale_color_identity(name = '',
#                        guide = "legend",
#                        labels = COLOR$position_name,
#                        breaks = COLOR$colors) +
#   geom_smooth(method = 'loess', alpha = 0.2, size = 1.5, color = 'gray') +
#   geom_label_repel(aes(label = ifelse(count >= 19, Player, ''),
#                        color = colors), force = 10, show.legend = F) +
#   labs(title = 'Weight & Height for the weekly award players', subtitle = 'size of point represents the over all number of weekly award')
# 

# df %>% group_by(newConference, Season.short, Real_value) %>% 
#   summarise(count = sum(Real_value)) %>% 
#   mutate(newCount = ifelse(newConference == 'East', 1*count, -1*count)) %>%
#   ggplot(aes(x = Season.short, y = newCount)) + 
#   geom_histogram(aes(fill = newConference), stat = 'identity', color = 'white') + 
#   theme_fivethirtyeight(16) + scale_fill_manual(name = '', values = c('#87CEFF', '#EE2C2C')) + 
#   scale_x_continuous(breaks = seq(1985,2018, by = 5)) + 
#   scale_y_continuous(breaks = seq(-20,20,5), labels = abs) + 
#   labs(title = 'number of weekly awards in East & West', subtitle = '')

custom_weeks <- c(38,42,46,50,1,5,9,13,17,21)
season_months <- c("Sept", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "June")

makeWeeklyChart <- function(player_name){
  temp <- df %>% filter(Player == player_name) %>% 
    group_by(Season.short,month_name,week,day) %>% summarize(week_count=n())
  temp$week <- factor(temp$week)
  temp$week <- factor(temp$week, levels = c(seq(40,52),seq(1,22)))
  temp$month_name <- as.factor(temp$month_name)
  temp$month_name <- factor(temp$month_name, levels = season_months)
  pal='B'
  ggplot(temp, aes(x = week, y = day, fill = week_count)) + 
    scale_fill_viridis(name = "count", 
                       option = pal,  # Variable color palette
                       direction = -1,  # Variable color direction
                       na.value = "grey93",
                       limits = c(0, max(temp$week_count))) +
    geom_tile(color = "white", size = 0.5) +
    facet_wrap("Season.short", ncol = 1) +
    scale_x_discrete(breaks = custom_weeks, labels = season_months) +
    theme_fivethirtyeight() +
    theme(axis.text.y = element_text(size=6),
          legend.position = "None",legend.direction='horizontal',
          legend.key.width = unit(0.5, "cm"),
          strip.text = element_text(hjust = 0, face = "bold", size = 8)) + 
    ggtitle(paste0(player_name,'\'s weekly award'))
}

