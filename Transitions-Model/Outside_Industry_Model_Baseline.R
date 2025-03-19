# Load the necessary libraries
library(ggplot2)
library(tidyr)
library(dplyr)

# Specify the file path
file_path <- '/Users/jillianmiles/Documents/Academic/Research/Data/Better Results/OOIAlooseResults.csv'

# Step 1: Read the CSV file into a dataframe
data <- read.csv(file_path)

# Step 2: Filter data for Ratio1 < 100
filtered_data <- data[data$Ratio1 < 40, ]

# Mapping of original names to logical nicknames
nickname_map <- list(
  "Industrial Machinery Mechanics" = "Ind Machinery Mech",
  "Production Workers, All Other" = "Prod Workers Other",
  "Multiple Machine Tool Setters, Operators, and Tenders, Metal and Plastic" = "Mult Tool Operators",
  "Metal-Refining Furnace Operators and Tenders" = "Metal Furnace Ops",
  "Furnace, Kiln, Oven, Drier, and Kettle Operators and Tenders" = "Kiln & Furnace Ops",
  "Computer Systems Analysts" = "Comp Sys Analysts",
  "Janitors and Cleaners, Except Maids and Housekeeping Cleaners" = "Janitors/Cleaners",
  "Metal Workers and Plastic Workers, All Other" = "Metal/Plastic Workers",
  "Secretaries and Administrative Assistants, Except Legal, Medical, and Executive" = "Admin Assistants",
  "Helpers--Electricians" = "Electrician Helpers",
  "Mixing and Blending Machine Setters, Operators, and Tenders" = "Mix/Blend Mach Ops",
  "Operating Engineers and Other Construction Equipment Operators" = "Const Equip Engrs",
  "Sheet Metal Workers" = "Sheet Metal Workers",
  "Machine Feeders and Offbearers" = "Mach Feeders",
  "Lathe and Turning Machine Tool Setters, Operators, and Tenders, Metal and Plastic" = "Lathe Mach Operators",
  "Industrial Truck and Tractor Operators" = "Truck/Tractor Ops",
  "Construction Laborers" = "Construction Laborers",
  "Human Resources Assistants, Except Payroll and Timekeeping" = "HR Assistants",
  "Stationary Engineers and Boiler Operators" = "Boiler Ops",
  "Chemical Plant and System Operators" = "Chem Plant Ops",
  "Heat Treating Equipment Setters, Operators, and Tenders, Metal and Plastic" = "Heat Treating Ops",
  "Office Clerks, General" = "Office Clerks",
  "Mechanical Drafters" = "Mechanical Drafters",
  "Structural Iron and Steel Workers" = "Iron/Steel Workers",
  "Foundry Mold and Coremakers" = "Foundry Coremakers",
  "Cutting and Slicing Machine Setters, Operators, and Tenders" = "Cut/Slice Mach Ops",
  "Structural Metal Fabricators and Fitters" = "Metal Fabricators",
  "Cleaning, Washing, and Metal Pickling Equipment Operators and Tenders" = "Metal Cleaning Ops",
  "Tank Car, Truck, and Ship Loaders" = "Tank/Truck Loaders",
  "Welding, Soldering, and Brazing Machine Setters, Operators, and Tenders" = "Weld/Solder Ops",
  "Extruding and Drawing Machine Setters, Operators, and Tenders, Metal and Plastic" = "Extruding Mach Ops",
  "Coating, Painting, and Spraying Machine Setters, Operators, and Tenders" = "Painting Mach Ops",
  "Milling and Planing Machine Setters, Operators, and Tenders, Metal and Plastic" = "Milling Mach Ops",
  "Molding, Coremaking, and Casting Machine Setters, Operators, and Tenders, Metal and Plastic" = "Molding Mach Ops",
  "Grinding, Lapping, Polishing, and Buffing Machine Tool Setters, Operators, and Tenders, Metal and Plastic" = "Polishing Mach Ops",
  "Production, Planning, and Expediting Clerks" = "Planning Clerks",
  "Chemical Technicians" = "Chemical Techs",
  "Helpers--Production Workers" = "Prod Worker Helpers",
  "Cutting, Punching, and Press Machine Setters, Operators, and Tenders, Metal and Plastic" = "Cut/Press Mach Ops",
  "Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products" = "Sales Reps",
  "Welders, Cutters, Solderers, and Brazers" = "Welders/Brazers",
  "Machinists" = "Machinists",
  "Laborers and Freight, Stock, and Material Movers, Hand" = "Freight Movers",
  "Rolling Machine Setters, Operators, and Tenders, Metal and Plastic" = "Rolling Mach Ops"
)

# Add a new column for nicknames by matching with the map
filtered_data$Nickname <- sapply(filtered_data$Description, function(x) nickname_map[[x]])






filtered_data <- filtered_data %>%
  arrange(desc(Ratio1)) %>%
  mutate(Nickname = factor(Nickname, levels = unique(Nickname)))  # Define factor levels







# Step 4: Reshape the data to long format
long_data <- filtered_data %>%
  gather(key = "JobType", value = "Value", AVGUNEMP, total_annual_non_replacement_jobs)






# Step 5: Create the grouped bar chart
ggplot(long_data, aes(x = Value, y = factor(Nickname), fill = JobType)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  scale_fill_manual(values = c("darkred", "#334099"),
                    labels = c("Unemployment (Avg Across Scenarios)", 
                               "Total Jobs in Occupation Opportunity Space")) +  # Relabel the legend
  labs(
    title = "Job Opportunities and Unemployment Across Occupations",
    x = "Total Jobs",
    y = "Occupation (shortened)",
    fill = "Variable"
  ) +
  scale_x_continuous(labels = scales::comma) + # Format x-axis labels
  theme_minimal() +
  theme(
    axis.text.y = element_text(hjust = 0),
    axis.text.x = element_text(size = 12),
    axis.title.x = element_blank(),
    axis.title.y = element_text(size = 14),
    legend.title = element_text(size = 10),
    legend.text = element_text(size = 10),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    legend.position = "top"  # Position the legend at the top
  )
