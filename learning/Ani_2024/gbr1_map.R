setwd("C:/Users/cani/OneDrive - Australian Institute of Marine Science/Desktop/RRAP/Moore_simulations/")
library(dplyr)
library(ggplot2)
library('ereefs')
library(ncdf4)
library('metR')
library(splancs)
#This script contains codes used to plot the domain and grids of RECOM and GBR1 hydrodynamic models, and the average velocities 

load('inputs/sysdata.rda')
gbr1_data = readRDS('inputs/u_gbr1.rds')
#plot RECOM and GBR1 cluster domain and grids

Long = c(gbr1_x_grid[145:200,1425:1480])
Lat = c(gbr1_y_grid[145:200,1425:1480])
gbr_subset = data.frame(lon = Long, lat = Lat)

recom_data = readRDS("inputs/u_spring.rds")
spatial = read.csv("inputs/moore_spatial.csv")
datshape <- gbr1_data[inout(gbr1_data[,3:4],gbr_subset,bound=TRUE),]

p = ggplot() + geom_polygon(datshape, mapping = aes(y=y, x=x,fill = value, group = id)) + 
  geom_path(datshape, mapping = aes(x =x,y = y, group = id), linewidth=0.6, color = "gray") +
  #geom_polygon(recom_data, mapping = aes(y=y, x=x,fill = value, group = id)) + 
  geom_path(recom_data, mapping = aes(x =x,y = y, group = id), linewidth=0.3, color = "black") +
  geom_point(data = spatial[1:334,], mapping = aes(x=lon, y=lat), size = 0.5, color = 'brown') +
  geom_rect(aes(xmin = 146.21, xmax = 146.245, ymin = -16.87, ymax = -16.84), color = "black", linewidth=1, alpha = 0) +
  xlab("Longitude") + ylab("Latitude") +
  coord_sf()+ #xlim(145.9,146.5681)+ ylim(-17.23685,-16.57687) + 
  scale_fill_distiller(palette = 'PuBu', name = expression(m~s^-1),
                       na.value="transparent") +
  theme_bw() + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.text.x = element_text(angle = 45, hjust=1),
                     axis.text=element_text(size=18), axis.title=element_text(size=18),#legend.position = 'none',
                     legend.text=element_text(size=18),legend.title=element_text(size=18))


p1 = ggplot() + #geom_polygon(datshape, mapping = aes(y=y, x=x,fill = value, group = id)) +
      geom_path(recom_data, mapping = aes(x =x,y = y, group = id), linewidth=0.3, color = "black") +
      geom_point(data = spatial[1:334,], mapping = aes(x=lon, y=lat), size = 0.8, color = 'brown') +
      scale_y_continuous(limits = c(-16.87, -16.84)) + scale_x_continuous(limits = c(146.21, 146.245)) +
     scale_fill_distiller(palette = 'PuBu',
                       na.value="transparent")  +
    theme_bw() + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), 
                       legend.position = 'none',
                       axis.title=element_blank(),
                       axis.text=element_blank(),
                       axis.ticks=element_blank())

# Combine the main plot with the zoomed plot
P = p + annotation_custom(ggplotGrob(p1), xmin = 145.9, xmax = 146.05, ymin = -16.7, ymax = -16.58) +
    geom_rect(aes(xmin = 145.9, xmax = 146.05, ymin = -16.7, ymax = -16.58), color='black', linewidth=1, linetype='dashed', alpha=0) +
    geom_path(aes(x,y,group=grp), 
            data=data.frame(x = c(146.21,145.9,146.245,146.05), y=c(-16.87,-16.7,-16.84,-16.58),grp=c(1,1,2,2)),
            color='black', linewidth=1, linetype='dashed')

ggsave(P, file='outputs/images/moore_gbr.png', width= 17.8, height = 15, units = "cm")





# extract and plot average velocities during  the dispersal period
datapoly_u = map_ereefs_movie (var_name = c("u"), 
                                start_date = c(2015,11,30), 
                                end_date = c(2015,12,31), 
                                layer = 'surface', 
                                output_dir = 'ToAnimate', 
                                Land_map = FALSE, 
                                input_file = "Moore_2015_simple.nc",
                                input_grid = "Moore_grid.nc", 
                                scale_col = c('ivory', 'coral4'), 
                                scale_lim = c(NA, NA), 
                                zoom = 6, 
                                box_bounds = c(NA, NA, NA, NA), 
                                suppress_print=TRUE, 
                                stride = 'daily',
                                verbosity=0, 
                                label_towns = TRUE,
                                strict_bounds = FALSE,
                                mark_points = NULL,
                                gbr_poly = FALSE,
                                add_arrows = FALSE,
                                max_u = NA,
                                scale_arrows = NA,
                                show_bathy=FALSE,
                                contour_breaks=c(5,10,20))

datapoly_v = map_ereefs_movie (var_name = c("v"), 
                               start_date = c(2015,11,30), 
                               end_date = c(2015,12,31), 
                               layer = 'surface', 
                               output_dir = 'ToAnimate', 
                               Land_map = FALSE, 
                               input_file = "Moore_2015_simple.nc",
                               input_grid = "Moore_grid.nc", 
                               scale_col = c('ivory', 'coral4'), 
                               scale_lim = c(NA, NA), 
                               zoom = 6, 
                               box_bounds = c(NA, NA, NA, NA), 
                               suppress_print=TRUE, 
                               stride = 'daily',
                               verbosity=0, 
                               label_towns = TRUE,
                               strict_bounds = FALSE,
                               mark_points = NULL,
                               gbr_poly = FALSE,
                               add_arrows = FALSE,
                               max_u = NA,
                               scale_arrows = NA,
                               show_bathy=FALSE,
                               contour_breaks=c(5,10,20))

mean_vel = sqrt(datapoly_u$datapoly$value ^ 2 + datapoly_v$datapoly$value ^ 2)

mean_velocity = transform(datapoly_u$datapoly, mean_vel = mean_vel, value_1 =datapoly_v$datapoly$value)

unique_vel = mean_velocity%>% distinct(id, .keep_all=TRUE)

p1 = ggplot(mean_velocity, aes(x = x, y = y)) + 
  geom_vector(data= unique_vel, aes(x = x, y = y, dx = value, dy = value_1), skip.x = 3, skip.y = 0, color = "black", arrow.type = "open") +
  coord_map(ylim = c(-16.935,-16.785), xlim = c(146.1675,146.302)) + 
  scale_mag(name = expression(atop(velocity,paste(~(m~s^-1)))), max_size = 1) + 
  xlab("Longitude") + ylab("Latitude") +
  scale_fill_distiller(name = expression(m~s^-1), palette = 'PuBu', na.value="transparent") +
  theme_bw() + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), 
                     axis.text=element_text(size=18), axis.title=element_text(size=18),
                     legend.text=element_text(size=18),legend.title=element_text(size=18))

ggsave(p1, file='moore_vel_2015.png')



