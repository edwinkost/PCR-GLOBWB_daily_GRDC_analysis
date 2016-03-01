
# packages needed and clear all available existing objects:
rm(list=ls()); # ls()

# global folder for all scenarios
global_folder = "/projects/0/wtrcycle/users/edwin/edwin/hyperhydro_november_2015/RhineMeuse/30min/"

first_run_to_be_analyzed = TRUE
for (i in seq(0,624,1)) {
ls 
# run code/name:
run_code = paste("code__a__",i,sep="")

# read table containing discharge analysis
discharge_table_file = paste(global_folder, run_code,"/analysis/daily_discharge_2008-2013/summary.txt",sep="") 
discharge_table = read.table(discharge_table_file, header=T, sep= ";")

#~ # select only a specific station:
#~ discharge_table = discharge_table[which(discharge_table$station_name == "LOBITH"), ]

######################################################################################################
# calculate performance values
#
# - using ns_efficiency_log
performance_per_river = discharge_table$ns_efficiency

# - set minimum value
min_value = 0.00
performance_per_river[which(performance_per_river < min_value)] = 0.0

# - average performance value
performance = sum(performance_per_river * discharge_table$grdc_catchment_area_in_km2, na.rm = T)
performance = performance / sum(discharge_table$grdc_catchment_area_in_km2, na.rm = T)

print(performance)

#
######################################################################################################



if (first_run_to_be_analyzed == TRUE) {
summary = cbind(run_code, performance)
first_run_to_be_analyzed = FALSE
} else {
summary = rbind(summary, 
          cbind(run_code, performance))
}
}


######################################################################################################
# convert performance summary table to data frame
summary_df = data.frame(summary)
summary_df$run_code             = as.character(summary_df$run_code)
summary_df$performance          = as.numeric(as.character(summary_df$performance))
######################################################################################################


########################################################################################################################
# merge it to parameters table
parameters = data.frame()
parameters = rbind(parameters, read.table("/home/edwin/github/edwinkost/hyperhydro_pcrglobwb/05min/table_15_november_2015_cartesius.txt", header=T)[1:5])            

# the first column is character
parameters[,1] = as.character(parameters[,1])

# reference run  
parameters = rbind(parameters, c("code__a__0", 1.0, 0.0, 0.0, 1.0))

# the first column is code
names(parameters)[1] <- "run_code"

# make sure formats are correct
parameters[,1] <- as.character(parameters[,1])
parameters[,2:ncol(parameters)] <- lapply(parameters[,2:ncol(parameters)], as.numeric)

final_table = merge(parameters, summary_df, by = "run_code")

########################################################################################################################

# order it based on performance values
final_table = final_table[order(-final_table$performance), ]
final_table[1:20,]

# write it to a txt file
write.table()


