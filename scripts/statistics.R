# Load the libraries
library(tidyverse)
library(broom)  

cat("Starting Analysis in R\n")

# 1. Load the data
df <- read_csv("data/processed/processed_data.csv", show_col_types = FALSE)

# 2. Convert categorical variables into Factors
df$group <- as.factor(df$group)
df$difficulty <- as.factor(df$difficulty)

cat("\n--------------------------------------------------\n")
cat("MODEL 1: Behavioral (Reaction Time)\n")
cat("--------------------------------------------------\n")
# Standard Linear Model for a 2x2 Factorial Design
model_rt <- lm(reaction_time_ms ~ group * difficulty, data = df)

# Print the ANOVA table to the console
print(anova(model_rt))

cat("\n--------------------------------------------------\n")
cat("MODEL 2: Physiological (HRV - RMSSD)\n")
cat("--------------------------------------------------\n")
# Standard Linear Model for Physiology
model_hrv <- lm(HRV_RMSSD ~ group * difficulty, data = df)

# Print the ANOVA table to the console
print(anova(model_hrv))

cat("\n--------------------------------------------------\n")
cat("Exporting Results for the Dashboard...\n")
cat("--------------------------------------------------\n")

# 3. Clean up the results using 'tidy' and save them as CSVs
tidy_rt <- tidy(model_rt)
tidy_hrv <- tidy(model_hrv)

write_csv(tidy_rt, "data/processed/stats_rt_results.csv")
write_csv(tidy_hrv, "data/processed/stats_hrv_results.csv")

cat("Analysis complete, Statistical tables saved to data/processed/\n")