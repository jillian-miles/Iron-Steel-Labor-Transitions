library(readxl)

# Set the file path
file_path <- "/Users/jillianmiles/Documents/Academic/Research/data/Better Results/Data for Charts 2.xlsx"

RCDFS <- read_excel(file_path, sheet = "RCDFS")
Hplots <- read_excel(file_path, sheet = "HPlots")
library(ggplot2)
library(patchwork)

# Assuming your data frame is named 'RCDFS'
# If your data is in a different format, adjust accordingly

# Create a custom theme with a light gray background
fancy_theme <- function(base_size = 12, base_family = "") {
  theme_minimal(base_size = base_size, base_family = base_family) +
    theme(
      plot.title = element_text(face = "bold", size = rel(1.5), hjust = 0.5),  # Center the big title
      axis.title = element_text(face = "bold"),
      axis.text = element_text(size = rel(0.8)),
      legend.position = "none",
      panel.background = element_rect(fill = "#F5F5F5")  # Light gray background
      
    )
}

# Define a darker blue color
darker_blue <- "#003366"
  
# Create individual line charts for each occupation with fancy theme
chart1 <- ggplot(RCDFS, aes(x = Similarity, y = `49-9041 | Industrial Machinery Mechanics`)) +
  geom_line(color = darker_blue) +
  labs(title = "Industrial Machinery Mechanics (6.4% of Workforce)", x = "Skill Level Sufficiency", y = "Number Occs Qualified For") +
  theme_minimal() +
  theme(
    plot.title = element_text(size = rel(1)),
    axis.title = element_text(size = rel(0.9)),
    axis.text = element_text(size = rel(0.9)),
    panel.background = element_rect(fill = "#F5F5F5")  # Light gray background
    
  )

chart2 <- ggplot(RCDFS, aes(x = Similarity, y = `51-4023 | Machine Setters, Operators, and Tenders, Metal and Plastic`)) +
  geom_line(color = darker_blue) +
  labs(title = "Machine Setters, Operators, and Tenders (7.5% of Workforce)", x = "Skill Level Sufficiency", y = "Number Occs Qualified For") +
  theme_minimal() +
  theme(
    plot.title = element_text(size = rel(1)),
    axis.title = element_text(size = rel(0.9)),
    axis.text = element_text(size = rel(0.9)),
    panel.background = element_rect(fill = "#F5F5F5")  # Light gray background
    
  )

chart3 <- ggplot(RCDFS, aes(x = Similarity, y = `51-1011 | First-Line Supervisors of Production and Operating Workers`)) +
  geom_line(color = darker_blue) +
  labs(title = "First-Line Supervisors of Production (5.0% of Workforce)", x = "Skill Level Sufficiency", y = "Number Occs Qualified For") +
  theme_minimal() +
  theme(
    plot.title = element_text(size = rel(1)),
    axis.title = element_text(size = rel(0.9)),
    axis.text = element_text(size = rel(0.9)),
    panel.background = element_rect(fill = "#F5F5F5")  # Light gray background
    
  )

chart4 <- ggplot(RCDFS, aes(x = Similarity, y = `53-7062 | Laborers and Freight, Stock, and Material Movers, Hand`)) +
  geom_line(color = darker_blue) +
  labs(title = "Laborers and Material Movers (3.7% of Workforce)", x = "Skill Level Sufficiency", y = "Number Occs Qualified For") +
  theme_minimal() +
  theme(
    plot.title = element_text(size = rel(1)),
    axis.title = element_text(size = rel(0.9)),
    axis.text = element_text(size = rel(0.9)),
    panel.background = element_rect(fill = "#F5F5F5")  # Light gray background
    
  )

# Arrange the individual charts in a 2x2 grid
combined_plot <- (chart1 | chart2) / (chart3 | chart4)

# Add a big title using plot_annotation()
combined_plot <- combined_plot +
  plot_annotation(title = "Skills Level Sufficiency Survival Curves for Iron and Steel Occupations", theme = fancy_theme())

# Display the combined plot
print(combined_plot)



library(ggplot2)
library(tidyr)

# Assuming your data frame is named 'Hplots'
# If your data is in a different format, adjust accordingly

# Reshape the data for ggplot
Hplots_long <- gather(Hplots, Response, Count, -SOC)
Hplots_long$Response <- factor(Hplots_long$Response, levels = rev(unique(Hplots_long$Response)))

# Trim the 'SOC' column to the first 7 characters
Hplots_long$SOC <- substr(Hplots_long$SOC, 1, 7)

science_nature_palette <- c("#e31a1c", "#1f78b4", "#ff7f00", "#b2df8a", "#6a3d9a", "#a6cee3", "#fb9a99", "#33a02c")

modified_palette <- c("#e41a1c", "#377eb8", "#4daf4a", "#ff7f00", "#a65628", "#984ea3", "#999999", "#f781bf")

muted_science_nature_palette <- c("#d57072", "#8197bb", "#e19280", "#c6dfb7", "#977eab", "#bdd6e9", "#fbc0c1", "#9ec594")

darker_science_nature_palette <- c("#99000d", "#08519c", "#cc4c02", "#238b45", "#4a1486", "#084594", "#ff7f00", "#006d2c")

adjusted_science_nature_palette <- c("#99000d", "#08519c", "#cc4c02", "#d73027", "#4a1486", "#084594", "#c51b7d", "#006d2c")

# Define a darker version of the Science/Nature-inspired color palette with more purple
adjusted_science_nature_palette <- c("#99000d", "#08519c", "#cc4c02", "#999999", "#4a1486", "#081534", "#9e1a76", "#006d2c")


# Create the horizontal stacked bar plot
plot_horizontal <- ggplot(Hplots_long, aes(x = Count, y = SOC, fill = Response, label = Count)) +
  geom_bar(stat = "identity", position = "stack", width = 0.7) +
  geom_text(position = position_stack(vjust = 0.5), size = 3, color = "white") +  # Add white data labels
  scale_fill_manual(values = adjusted_science_nature_palette) +  # Use The Economist-inspired color palette
  labs(title = "Limiting Factor in Job Transferability",
       x = "Count",
       y = "SOC") +
  theme_minimal() +
  theme(
    legend.position = "bottom",
    legend.title = element_blank(),
    axis.text = element_text(size = 12, hjust = 0),
    axis.title = element_text(size = 12, face = "bold"),
    plot.title = element_text(size = 16, face = "bold", hjust = 0.5),
    legend.text = element_text(size = 10),
    axis.ticks.y = element_blank(),  # Remove y-axis ticks
    panel.grid.major.x = element_line(color = "white"),  # Remove vertical gridlines
    panel.grid.minor.x = element_line(color = "white"),  # Remove vertical gridlines
    panel.background = element_rect(fill = "#F5F5F5")  # Light gray background
  )

# Display the plot
print(plot_horizontal)