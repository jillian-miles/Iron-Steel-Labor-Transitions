
#import excel sheet from this location '/Users/jillianmiles/Documents/Academic/Research/data/Better Results/Data for Charts .xlsx'

#Save each sheet as a dataframe


# Install and load the readxl package if not already installed
# install.packages("readxl")
library(readxl)

# Set the file path
file_path <- "/Users/jillianmiles/Documents/Academic/Research/data/Better Results/Data for Charts .xlsx"

sorted_demand_remaining <- read_excel(file_path, sheet = "Demand Remaining")
jobs_transitioned <- read_excel(file_path, sheet = "Jobs Transitioned")
by_soc_ap <- read_excel(file_path, sheet = "By SOC AP")
attempt_at_box <- read_excel(file_path, sheet = "Jobs Transitioned Three")
attempt_at_box2 <- read_excel(file_path, sheet = "Jobs Transitioned Two")


# Install and load the ggplot2 package if not already installed
# install.packages("ggplot2")
library(ggplot2)

# Assuming you've already loaded your data frame with the sheet "by soc ap" into a variable named 'by_soc_ap'
# You can aggregate the data by SOC Category and calculate the average values
agg_data <- aggregate(cbind(`Supply Remaining`, `Percent Remaining`) ~ `SOC Category`, data = by_soc_ap, FUN = mean)

# Create a bar chart for the average "Supply Remaining" on the primary y axis
# and a line chart for the average "Percent Remaining" on the secondary y axis
plot <- ggplot(agg_data, aes(x = `SOC Category`)) +
  geom_bar(aes(y = `Supply Remaining`), stat = "identity", fill = "#335577") +  # Dark gray fill color
  geom_line(aes(y = `Percent Remaining` * max(agg_data$`Supply Remaining`), group = 1), color = "RED", size = 1.5) +  # Red line color
  geom_text(aes(x = tail(`SOC Category`, 1), y = tail(`Percent Remaining` * max(agg_data$`Supply Remaining`), 1), label = "Percent Remaining"), vjust = 1, hjust = 3, color = "RED", size = 4) +  # Add label for the red line
  scale_y_continuous("Supply Mass Remaining (Jobs not Transitioned)", sec.axis = sec_axis(~./max(agg_data$`Supply Remaining`), name = " ")) +
  labs(title = "Average Supply Mass of Jobs Not Transitioned by Occupational Category") +
  labs(x = "SOC Category") +  # X-axis label
  theme_minimal() +
  theme(
    plot.title = element_text(size = 16, face = "bold", hjust = 0.5),
    axis.title.x = element_text(size = 14, face = "bold"),  # Bold x-axis label
    axis.title.y = element_text(size = 14, face = "bold"),
    axis.text.x = element_text(size = 14, angle = 45, hjust = 1, vjust = 1, face = "bold"),  # Bold x-axis labels
    axis.text.y = element_text(size = 12),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill = "#F5F5F5"),  # Light gray background
    plot.background = element_rect(fill = "white"),  # White plot background
    legend.position = "none"  # No legend
  )

# Display the plot
print(plot)


# Assuming you've already loaded your data frame with the sheet "Jobs Transitioned" into a variable named 'jobs_transitioned'

# Create a grouped bar plot for "Sum of Transitioned"
# Reshape the data into long format
library(tidyr)

long_data <- pivot_longer(jobs_transitioned, cols = c("Sum of Transitioned", "Sum of Supply Remaining"), names_to = "Variable", values_to = "Value")

# Create a stacked bar plot
plot_combined <- ggplot(long_data, aes(x = `Scenario Trial`, y = Value, fill = Variable)) +
  geom_bar(stat = "identity", color = "white", position = "stack", width = 0.7) +
  labs(title = "Sum of Supply Remaining and Transitioned by Scenario and Trial",
       x = "Scenario and Trial",
       y = "Sum of Jobs") +
  scale_fill_manual(values = c("Sum of Transitioned" = "#404040", "Sum of Supply Remaining" = "#8B0000")) +
  theme_minimal() +
  theme(
    legend.position = "bottom",
    axis.text.x = element_text(angle = 45, hjust = 1, size = 12),
    plot.title = element_text(size = 16, face = "bold", hjust = 0.5),
    axis.title.x = element_text(size = 14, face = "bold"),
    axis.title.y = element_text(size = 14, face = "bold"),
    axis.text.y = element_text(size = 12),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill = "#F5F5F5"),
    plot.background = element_rect(fill = "white")
  )

# Display the updated plot
print(plot_combined)





# in this df: sorted_demand_remaining <- read_excel(file_path, sheet = "Demand Remaining")
# make a new df which aggregate the column'Demand Remaining" by 'Scenario Trial' and just has those 2 cols.  


# Load the dplyr package for data manipulation
# install.packages("dplyr")
library(dplyr)

# Aggregate "Demand Remaining" by "Scenario Trial"
agg_demand_remaining <- sorted_demand_remaining %>%
  group_by(`Scenario Trial`) %>%
  summarise(`Sum of Demand Remaining` = sum(`Demand Rem`))

# Display the new aggregated data frame
print(agg_demand_remaining)

merged_df <- jobs_transitioned %>%
  left_join(agg_demand_remaining, by = "Scenario Trial")

merged_df[c(13, 14, 15, 16), "Sum of Demand Remaining"] <- c(0, 36, 168, 0)

#merged_df new col which is sum of `Sum of Transitioned` and `Sum of Demand Remaining`
merged_df <- merged_df %>%
  mutate(`Sum of Transitioned and Demand Remaining` = `Sum of Transitioned` + `Sum of Demand Remaining`)

# Display the updated data frame
print(merged_df)


# Your new data
new_data <- data.frame(
  "Scenario Trial" = c("2xEAFDRI 1", "2xEAFDRI 2", "2xEAFDRI 3", "2xEAFDRI 4", "2xEAFDRI 5", "2xEAFDRI 6"),
  "Sum of Transitioned" = c(721, 1130, 1280, 707, 620, 671),
  "Sum of Supply Remaining" = c(2129, 1720, 1570, 2143, 2230, 2179),
  "Sum of Demand Remaining" = c(1, 12, 1, 2, 1, 1),
  "Sum of Transitioned and Demand Remaining" = c(722, 1142, 1281, 709, 621, 672)
)

colnames(new_data) <- colnames(merged_df)


# Add the new data to the existing data frame
merged_df <- rbind(merged_df, new_data)





plot_combined <- ggplot(merged_df, aes(x = `Scenario Trial`)) +
  geom_bar(aes(y = `Sum of Transitioned`), stat = "identity", color = "white", fill = "#404040", width = 0.7) +
  geom_point(aes(y = `Sum of Transitioned and Demand Remaining`, color = "Max Possible Transitioned"), size = 15, shape = 95) +
  geom_hline(yintercept = 2850, linetype = "solid", color = "darkblue", size = 2) +
  labs(title = "Simulated and Maximum Transitioned Workers by Scenario and Trial",
       x = "Scenario and Trial",
       y = "Number of Transitioned Workers") +
  scale_y_continuous(sec.axis = sec_axis(~., name = "Maximum Possible Transitioned")) +
  scale_color_manual(values = c("Max Possible Transitioned" = "red")) +
  theme_minimal() +
  theme(
    plot.title = element_text(size = 16, face = "bold", hjust = 0.5),
    axis.title.x = element_text(size = 14, face = "bold"),  # Bold x-axis label
    axis.title.y = element_text(size = 14, face = "bold"),
    axis.text.x = element_text(size = 14, angle = 45, hjust = 1, vjust = 1, face = "bold"),  # Bold x-axis labels
    axis.text.y = element_text(size = 12),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.background = element_rect(fill = "#F5F5F5"),  # Light gray background
    plot.background = element_rect(fill = "white"),  # White plot background
    legend.position = "bottom",  # Position the legend at the bottom
    legend.title = element_blank()  # Remove legend title
  )

# Display the combined plot
print(plot_combined)



# Convert Scenario to a factor with a specific order
attempt_at_box$Scenario <- factor(attempt_at_box$Scenario, levels = c("1x Scaled EAF", "2x EAF", "2x EAF DRI", "BAU", "Closure"))

# Plotting
ggplot(attempt_at_box, aes(x = Scenario, y = Average, fill = Category)) +
  geom_boxplot(position = "dodge", alpha = 0.7, outlier.shape = NA) +
  geom_jitter(position = position_dodge(width = 0.75), size = 2, alpha = 0.7) +
  stat_summary(fun.y = "mean", geom = "point", position = position_dodge(width = 0.75), color = "black", size = 3) +
  labs(title = "Jobs Transitioned and Remaining Supply Mass",
       x = "Scenario",
       y = "Average",
       fill = "Category") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  scale_fill_manual(values = c("Jobs Transitioned" = "blue", "Remaining Supply Mass" = "red"))




# Convert Scenario to a factor with a specific order
attempt_at_box2$Scenario <- factor(attempt_at_box2$Scenario, levels = c("1x Scaled EAF", "2x EAF", "2x EAF DRI", "BAU", "Closure"))
# Reshape the data to long format if needed (using tidyr::gather)

library(tidyr)
attempt_at_box2_long <- gather(attempt_at_box2, key = "variable", value = "value", -Scenario)
attempt_at_box2_long$variable <- factor(attempt_at_box2_long$variable, levels = c("Sum of Transitioned", "Sum of Supply Remaining"))


attempt_at_box2_long <- attempt_at_box2_long %>%
  filter(variable != "Sum of Transitioned")


# Plotting with a sleek theme
newist <- ggplot(attempt_at_box2_long, aes(x = Scenario, y = value, fill = variable)) +
  geom_boxplot(position = position_dodge(width = 0.8), alpha = 0.7, fill = "darkred") +  # Slightly darker reddish-pink for boxes
  labs(
    title = "Simulated Remaining Worker Supply Mass by Scenario",
    x = "Scenario",
    y = "Number of Workers Remaining in Supply \n (simulated number of jobs lost in transition)"
  ) +
  theme_minimal() +
  theme(
    panel.background = element_rect(fill = "#F0F0F0"),
    panel.grid.major = element_blank(),  # Remove major gridlines
    panel.grid.minor = element_blank(),  # Remove minor gridlines
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),  # Center title
    axis.title.x = element_text(size = 14, face = "bold"),  # Bold x-axis label
    axis.title.y = element_text(size = 14, face = "bold"),
    axis.text.x = element_text(size = 14, angle = 20, hjust = 1, vjust = 1, face = "bold"),  # Bold x-axis labels
    axis.text.y = element_text(size = 12),
    legend.position = "none",  # Remove legend
  )

print(newist)





