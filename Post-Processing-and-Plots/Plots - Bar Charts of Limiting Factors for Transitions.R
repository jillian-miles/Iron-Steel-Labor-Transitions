library(openxlsx)
library(ggplot2)
library(dplyr)


# Load the data
comparison_df <- read.xlsx('/Users/jillianmiles/Documents/Academic/Research/Data/Results I guess/SOC_Comparisons.xlsx', sheet = 1)

# Melt the data for easier plotting
melted_data <- reshape2::melt(comparison_df, id.vars = c("SOC1", "SOC2"))

# Aggregate data by SOC1
summary_data <- comparison_df %>%
  group_by(SOC1) %>%
  summarize(
    Y_Skill_Importance = sum(Skill_Importance == "Y"),
    N_Skill_Importance = sum(Skill_Importance == "N"),
    Y_Skill_Level = sum(Skill_Level == "Y"),
    N_Skill_Level = sum(Skill_Level == "N"),
    Y_Abilities_Importance = sum(Abilities_Importance == "Y"),
    N_Abilities_Importance = sum(Abilities_Importance == "N"),
    Y_Abilities_Level = sum(Abilities_Level == "Y"),
    N_Abilities_Level = sum(Abilities_Level == "N"),
    Y_Knowledge_Importance = sum(Knowledge_Importance == "Y"),
    N_Knowledge_Importance = sum(Knowledge_Importance == "N"),
    Y_Knowledge_Level = sum(Knowledge_Level == "Y"),
    N_Knowledge_Level = sum(Knowledge_Level == "N"),
    Y_Salary = sum(Salary == "Y"),
    N_Salary = sum(Salary == "N")
    # Add similar lines for other columns you want to summarize
  )


# in the summary data
# ignoring the importance columns (just include the level, and salary data)
# can we summarize the data by the first two chars of the SOC1 col 
# where what we are looking for is the average number for each of the cols across all SOC1 with same first 2 chars 
# then can we plot that data in a stacked bar chart?
# where we have groupings for each of the SOC1 Chars on the x axis, 
# and the bars are stacked like ability level yes below ability level nos so we can see the differences between different metrics for a SOC1 cat
# and the comparison across the different SOC groups? 

# Assuming your summary_data is already loaded and contains necessary columns

# Assuming your summary_data is already loaded and contains necessary columns

# Assuming your summary_data is already loaded and contains necessary columns

# Extract first two characters of SOC1
summary_data$SOC1_Group = substr(summary_data$SOC1, 1, 2)

# Summarize the data by SOC1_Group
summary_by_group = summary_data %>%
  group_by(SOC1_Group) %>%
  summarize(
    Y_Salary = mean(Y_Salary),
    N_Salary = mean(N_Salary),
    Y_Skill_Level = mean(Y_Skill_Level),
    N_Skill_Level = mean(N_Skill_Level),
    Y_Abilities_Level = mean(Y_Abilities_Level),
    N_Abilities_Level = mean(N_Abilities_Level),
    Y_Knowledge_Level = mean(Y_Knowledge_Level),
    N_Knowledge_Level = mean(N_Knowledge_Level)
  )

# Melt the data for easier plotting
library(reshape2)

filtered_summary <- summary_by_group %>%
  filter(as.numeric(SOC1_Group) %in% c(11:19, 46:53))

summary_melted <- melt(filtered_summary, id.vars = "SOC1_Group")

# Plot stacked bar chart for Y_Salary and N_Salary
library(ggplot2)
salary_plot <- ggplot(summary_melted %>% filter(variable %in% c("Y_Salary", "N_Salary")),
                      aes(x = SOC1_Group, y = value, fill = variable)) +
  geom_bar(stat = "identity", position = "stack", width = 0.7) +
  labs(title = "Salary as a Limiting Factor",
       x = "SOC Category",
       y = "Number of Occupations \n (avg across SOC Category)" ) + 
  scale_fill_manual(values = c("Y_Salary" = "lightblue", "N_Salary" = "darkred"),
                    labels = c("Y_Salary" = "Share Qualified", "N_Salary" = "Share Limiting Factor")) +
  theme_minimal()

# Plot stacked bar chart for Y_Skill_Level and N_Skill_Level
skill_plot <- ggplot(summary_melted %>% filter(variable %in% c("Y_Skill_Level", "N_Skill_Level")),
                     aes(x = SOC1_Group, y = value, fill = variable)) +
  geom_bar(stat = "identity", position = "stack", width = 0.7) +
  labs(title = "Skill Level as a Limiting Factor",
       x = "SOC Category",
       y = "Number of Occupations \n (avg across SOC Category)" ) + 
  scale_fill_manual(values = c("Y_Skill_Level" = "lightblue", "N_Skill_Level" = "darkred"),
                    labels = c("Y_Skill_Level" = "Share Qualified", "N_Skill_Level" = "Share Limiting Factor")) +
  theme_minimal()

# Plot stacked bar chart for Y_Abilities_Level and N_Abilities_Level
abilities_plot <- ggplot(summary_melted %>% filter(variable %in% c("Y_Abilities_Level", "N_Abilities_Level")),
                         aes(x = SOC1_Group, y = value, fill = variable)) +
  geom_bar(stat = "identity", position = "stack", width = 0.7) +
  labs(title = "Abilities Level as a Limiting Factor",
       x = "SOC Category",
       y = "Number of Occupations \n (avg across SOC Category)" ) + 
  scale_fill_manual(values = c("Y_Abilities_Level" = "lightblue", "N_Abilities_Level" = "darkred"),
                    labels = c("Y_Abilities_Level" = "Share Qualified", "N_Abilities_Level" = "Share Limiting Factor")) +
  theme_minimal()

# Plot stacked bar chart for Y_Knowledge_Level and N_Knowledge_Level
knowledge_plot <- ggplot(summary_melted %>% filter(variable %in% c("Y_Knowledge_Level", "N_Knowledge_Level")),
                         aes(x = SOC1_Group, y = value, fill = variable)) +
  geom_bar(stat = "identity", position = "stack", width = 0.7) +
  labs(title = "Knowledge Level as a Limiting Factor",
       x = "SOC Category",
       y = "Number of Occupations \n (avg across SOC Category)" ) + 
  scale_fill_manual(values = c("Y_Knowledge_Level" = "lightblue", "N_Knowledge_Level" = "darkred"),
                    labels = c("Y_Knowledge_Level" = "Share Qualified", "N_Knowledge_Level" = "Share Limiting Factor")) +
  theme_minimal()

# Arrange the plots together
library(patchwork)
combined_plots <- salary_plot + skill_plot + abilities_plot + knowledge_plot +
  plot_layout(ncol = 1)
combined_plots






# now i want to create a horizontal bar plot
# going through the original comparison_df let's take out only data where SOC1 = 53-7062 51-4023. 51-1011, or 49-9041
# temporarily ignore salary columns and the skill_importance, ability_importance, and knowledge_importance 
# for each of these, i want to calculate the following metrics:
  # how many rows have only Ys
  # How many have a N just in Skill Level
  # how many just N in Ability Level
  # N in knowledge level
  # N in both skill and knowedlge
  # both knowledge and ability
  # ability and skill
  # and then all 3 
# then i want a horizontal bar chart showing the results for each of the SOC with what percent and raw number was in each of these categories 
# Define the SOC1 values you want to analyze
# Define the SOC1 values you want to analyze
soc1_values <- c("53-7062", "51-4023", "51-1011", "49-9041")

# Filter data to keep only the relevant columns and rows
comparison_df_filtered <- comparison_df[comparison_df$SOC1 %in% soc1_values, c("SOC1","SOC2","Skill_Level", "Abilities_Level", "Knowledge_Level")]

# Initialize an empty data frame to store the cleaned results
cleaned_df <- data.frame()

# Loop through each SOC1 value
for (soc1_value in soc1_values) {
  
  # Filter data for the current SOC1
  soc1_data <- comparison_df_filtered[comparison_df_filtered$SOC1 == soc1_value, ]
  
  # Keep only the relevant columns (adjust column indices if needed)
  soc1_data <- soc1_data[, c("Skill_Level", "Abilities_Level", "Knowledge_Level")]
  
  # Calculate the metrics
  y_only <- sum(rowSums(soc1_data == "Y") == ncol(soc1_data))
  n_skill_level <- sum(soc1_data$Skill_Level == "N" & soc1_data$Abilities_Level == "Y" & soc1_data$Knowledge_Level == "Y")
  n_abilities_level <- sum(soc1_data$Skill_Level == "Y" & soc1_data$Abilities_Level == "N" & soc1_data$Knowledge_Level == "Y")
  n_knowledge_level <- sum(soc1_data$Skill_Level == "Y" & soc1_data$Abilities_Level == "Y" & soc1_data$Knowledge_Level == "N")
  n_skill_and_knowledge_level <- sum(soc1_data$Skill_Level == "N" & soc1_data$Abilities_Level == "Y" & soc1_data$Knowledge_Level == "N")
  n_abilities_and_knowledge_level <- sum(soc1_data$Skill_Level == "Y" & soc1_data$Abilities_Level == "N" & soc1_data$Knowledge_Level == "N")
  n_abilities_and_skill_level <- sum(soc1_data$Skill_Level == "N" & soc1_data$Abilities_Level == "N" & soc1_data$Knowledge_Level == "Y")
  n_all <- sum(soc1_data$Skill_Level == "N" & soc1_data$Abilities_Level == "N" & soc1_data$Knowledge_Level == "N")
  
  # Create a data frame with the results
  result_row <- data.frame(
    SOC1 = soc1_value,
    Y_only = y_only,
    N_Skill_Level = n_skill_level,
    N_Abilities_Level = n_abilities_level,
    N_Knowledge_Level = n_knowledge_level,
    N_Skill_Level_and_N_Knowledge_Level = n_skill_and_knowledge_level,
    N_Abilities_Level_and_N_Knowledge_Level = n_abilities_and_knowledge_level,
    N_Abilities_Level_and_N_Skill_Level = n_abilities_and_skill_level,
    N_all = n_all
  )
  
  # Append the results to the main cleaned data frame
  cleaned_df <- rbind(cleaned_df, result_row)
}

# Print the cleaned data frame
print(cleaned_df)


# Define the colors for different metrics
colors <- c(
  "Y_only" = "#66c2a5",
  "N_Skill_Level" = "#8da0cb",
  "N_Abilities_Level" = "#a6d854",
  "N_Knowledge_Level" = "red",
  "N_Skill_Level_and_N_Knowledge_Level" = "#fc8d62",
  "N_Abilities_Level_and_N_Knowledge_Level" = "#e78ac3",
  "N_Abilities_Level_and_N_Skill_Level" = "#ffd92f",
  "N_all" = "blue"
)

colors4 <- c(
  "Y_only" = "#335577",                               # Darker Dark Blue
  "N_Skill_Level" = "#99c2ff",                        # Light Blue
  "N_Abilities_Level" = "#bfbfb1",                    # Gray
  "N_Knowledge_Level" = "#666666",                    # Dark Red
  "N_Skill_Level_and_N_Knowledge_Level" = "lightblue", # Orange-Red
  "N_Abilities_Level_and_N_Knowledge_Level" = "blue", # Light Purple
  "N_Abilities_Level_and_N_Skill_Level" = "red", # Yellow
  "N_all" = "#990000"                                 # Darker Dark Blue (same as the first)
)



# Reverse the order of SOC1 levels
cleaned_df$SOC1 <- factor(cleaned_df$SOC1, levels = rev(unique(cleaned_df$SOC1)))

# Melt the data for easier plotting
library(reshape2)
cleaned_df_melted <- melt(cleaned_df, id.vars = "SOC1")

ggplot(cleaned_df_melted, aes(x = value, y = SOC1, fill = variable, label = value)) +
  geom_bar(stat = "identity", position = position_stack(reverse = TRUE), width = 0.7) +
  labs(title = "Limiting Factor for Transitioning - SKAs",
       x = "Occupations for Transitioning Into",
       y = "Origin Occupation") +
  scale_fill_manual(values = colors4, name = "Categories", labels = c(
    "Y_only" = "Qualified",
    "N_Skill_Level" = "Limited (Skill)",
    "N_Abilities_Level" = "Limited (Abilities)",
    "N_Knowledge_Level" = "Limited (Knowledge)",
    "N_Skill_Level_and_N_Knowledge_Level" = "Limited (Skills + Knowledge)",
    "N_Abilities_Level_and_N_Knowledge_Level" = "Limited (Abilities + Knowledge",
    "N_Abilities_Level_and_N_Skill_Level" = "Limited (Skills + Abilities",
    "N_all" = "Limited - All"
  )) +  # Updated legend title and labels  
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 16, hjust = 0.5),
    axis.title.y = element_text(face = "bold", size = 14),
    axis.title.x = element_text(face = "bold", size = 14),
    axis.text = element_text(size = 12),
    legend.title = element_text(face = "bold", size = 12),
    legend.text = element_text(size = 10),
    legend.position = "bottom",
    legend.key = element_rect(fill = "white", color = "white")  # Hide legend background
  ) +
  guides(fill = guide_legend(title = "Categories"))  # Updated legend variable title



soc1_values <- c("53-7062", "51-4023", "51-1011", "49-9041")

# Filter data to keep only the relevant columns and rows
comparison_df_filtered2 <- comparison_df[comparison_df$SOC1 %in% soc1_values, c("SOC1", "SOC2", "Skill_Level", "Abilities_Level", "Knowledge_Level", "Salary")]

# Initialize an empty data frame to store the cleaned results
cleaned_df2 <- data.frame()

# Loop through each SOC1 value
for (soc1_value in soc1_values) {
  
  # Filter data for the current SOC1
  soc1_data <- comparison_df_filtered2[comparison_df_filtered2$SOC1 == soc1_value, ]
  
  # Keep only the relevant columns (adjust column indices if needed)
  soc1_data <- soc1_data[, c("Skill_Level", "Abilities_Level", "Knowledge_Level", "Salary")]
  
  # Calculate the metrics
  y_only <- sum(rowSums(soc1_data == "Y") == ncol(soc1_data))
  n_SKA <- sum(soc1_data$Salary == "Y" & (soc1_data$Skill_Level == "N" | soc1_data$Abilities_Level == "N" | soc1_data$Knowledge_Level == "N"))
  n_SAL <- sum(soc1_data$Salary == "N" & (soc1_data$Skill_Level == "Y" & soc1_data$Abilities_Level == "Y" & soc1_data$Knowledge_Level == "Y"))
  n_Both <- sum(soc1_data$Salary == "N" & (soc1_data$Skill_Level == "N" | soc1_data$Abilities_Level == "N" | soc1_data$Knowledge_Level == "N"))
  
  # Create a data frame with the results
  result_row <- data.frame(
    SOC1 = soc1_value,
    Y_only = y_only,
    No_Sal = n_SAL,
    No_SKA = n_SKA,
    No_Both = n_Both
  )
  
  # Append the result to the cleaned data frame
  cleaned_df2 <- rbind(cleaned_df2, result_row)
}



# Define the colors for different metrics
colors2 <- c(
  "Y_only" = "#66c2a5",
  "No_Sal" = "#8da0cb",
  "No_SKA" = "#a6d854",
  "No_Both" = "red"
)

colors3 <- c(
  "Y_only" = "#335577",   # Darker Dark Blue
  "No_Sal" = "#99c2ff",   # Light Blue
  "No_SKA" = "#bfbfbf",   # Gray
  "No_Both" = "#990000"   # Dark Red
)



# Reverse the order of SOC1 levels
cleaned_df2$SOC1 <- factor(cleaned_df2$SOC1, levels = rev(unique(cleaned_df2$SOC1)))

# Melt the data for easier plotting
cleaned_df_melted2 <- melt(cleaned_df2, id.vars = "SOC1")

# Plot horizontal bar chart with data labels, reversed order, and a fancy theme
ggplot(cleaned_df_melted2, aes(x = value, y = SOC1, fill = variable, label = value)) +
  geom_bar(stat = "identity", position = position_stack(reverse = TRUE), width = 0.7) +
  labs(title = "Limiting Factor for Transitioning - SKAs with Wages",
       x = "Possible Destination Occupations",
       y = "Origin Occupation") +
  scale_fill_manual(values = colors3, name = "Categories", labels = c(
    "Y_only" = "Qualified",
    "No_Sal" = "Limited (Wages)",
    "No_SKA" = "Limited (SKA)",
    "No_Both" = "Limited (Both)"
  ))+
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 16, hjust = 0.5),
    axis.title.y = element_text(face = "bold", size = 14),
    axis.title.x = element_text(face = "bold", size = 14),
    axis.text = element_text(size = 12),
    legend.title = element_text(face = "bold", size = 12),
    legend.text = element_text(size = 10),
    legend.position = "bottom"
  )





